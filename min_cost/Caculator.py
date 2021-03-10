# -*-coding:utf-8 -*-
"""
本文件负责计算请求的部署节点以及利润
"""
import sys
import config
import copy

from Manager import manager
from DataCenter import DataCenter
from Request import Request
from Edge import Edge
from Graph import Graph
from Path import Path


def cmp(x, y):
    if x < y:
        return -1
    elif x == y:
        return 0
    else:
        return 1

class Caculator:
    def __init__(self) -> None:
        super().__init__()
        self.paths_pair = dict()  # <路径向量：Path实例>
        self.nodes = set()  # 最后得到的所需节点
        self.edges = set()  # 最后得到的所需链路<链路名：Edge实例>
        self.P_is = dict() # 元素为req_id:P_i
        self.L_is = dict()  # 元素为req_id:L_i

    # 计算请求的利润和部署的节点
    # 如果利润不为正，部署节点为0
    def calculate_hardware(self) -> None:
        for req in manager.requests:
            self.choose_path(req)
        paths = self.paths_pair.values()
        paths = list(paths)
        for p in paths:
            self.path_weight(p)
        paths = sorted(paths, key=lambda p: -p.weight)
        temp_reqs = set()
        for p in paths:
            p: Path
            # print("{}'s weight is {}".format(p.vec, p.weight))
            for req in p.requests:
                req:Request
                if req in temp_reqs:
                    continue
                temp_reqs.add(req)
                if p.vec not in req.path_vec or len(req.path_vec) <= 1:
                    continue
                self.del_edgecount(p.vec, req)
                self.del_node(p.vec, req)

        for node in manager.nodes.values():
            node:DataCenter
            if len(node.requests) > 0:
                self.nodes.add(node)
                self.get_node_cost(node)
        for e in manager.edges.values():
            e: Edge
            if len(e.requests) > 0:
                self.edges.add(e)
                self.get_edge_cost(e)

    def get_node_cost(self, node: DataCenter):
        node.cpu = 0
        node.cost = 0
        if len(node.requests) == 0:
            return
        for r in node.requests:
            r: Request
            node.cpu += r.process_source[node.id]
        node.cost = node.cpu * node.unitCpuPrice
        gain = self.node_gain(node)
        node.cpu *= (1-gain/node.cost)
        node.cost -= gain


    def get_edge_cost(self, edge: Edge):
        edge.bandWidth = 0
        edge.cost = 0
        if len(edge.requests) == 0:
            return
        for r in edge.requests:
            r: Request
            edge.bandWidth += r.bandwidth
        edge.cost = edge.bandWidth * edge.unitprice
        gain = self.link_gain(edge)
        edge.bandWidth *= (1-gain/edge.cost)
        edge.cost -= gain

    # 判断是否存在环
    def has_circle(self, vec:tuple):
        points = set()
        for i in vec:
            if i not in points:
                points.add(i)
            else:
                return True
        return False

    # 返回目标路径
    def choose_path(self, req: Request):
        for node in manager.nodes.values():
            node: DataCenter
            _,pre_half, pre_delay = Graph().get_shortest_path(req.src, node.id)
            pre_half = pre_half[::-1]
            _,second_half, second_delay = Graph().get_shortest_path(node.id, req.dst)
            second_half = second_half[::-1]
            path_vec = pre_half + second_half[1:]
            path_vec = tuple(path_vec)
            if self.has_circle(path_vec):
                continue
            # print("src = " + str(req.src) + " dst = "+ str(req.dst))
            if path_vec not in self.paths_pair:
                path = Path(path_vec, pre_delay + second_delay)
                if not self.check_constraints(req, path, node):
                    continue
                self.paths_pair[path_vec] = path
            else:
                path: Path = self.paths_pair[path_vec]
                if not self.check_constraints(req, path, node):
                    continue

    # 计算每条可用路径的选择权重
    def path_weight(self, path: Path) -> None:
        C_v: float = 1
        for v in path.nodes:
            v: DataCenter
            # C_v += v.cost - self.node_gain(v)
            C_v += v.cost
        C_e = 0
        for e in path.edges:
            e: Edge
            # C_e += e.cost - self.link_gain(e)
            C_e += e.cost
        path.weight = len(path.requests) / (C_v + C_e)

    def check_constraints(self, req: Request, path: Path, node: DataCenter) -> bool:
        # 检查时延
        if path.propagation_delay >= req.maxDelay:
            # print("req_id {} failed because delay".format(req.id))
            # print("maxDelay = {}, pdealy = {}".format(req.maxDelay, path.propagation_delay))
            return False
        # 处理时延
        process_delay = min(
            req.maxDelay - path.propagation_delay, len(req.sfc)*req.bandwidth)
        # 判断算力是否满足条件
        # 所需最低算力
        process_source = 0
        for vnf in req.sfc:
            process_source += config.VNF_DELAY[vnf]
        process_source *= 1/process_delay
        # 判断是否有足够算力
        # 没有可部署的节点，返回False
        req.process_source[node.id] = process_source
        node.requests.add(req)
        req.path_vec.add(path.vec)
        path.requests.add(req)
        for e in path.edges:
            e: Edge
            e.cost += req.bandwidth*e.unitprice
            manager.edges[e.id].requests.add(req)
        return True

    def link_gain(self, e: Edge) -> float:
        if len(e.requests) == 0:
            return 0
        multiplex_seq = [0 for _ in range(config.DURATION)]
        maxband = 0
        for r in e.requests:
            r: Request
            for i in range(config.DURATION):
                multiplex_seq[i] += r.bandSeq[i]
            maxband += r.bandwidth
        gain_band = sys.maxsize
        for i in range(config.DURATION):
            gain_band = min(gain_band, maxband-multiplex_seq[i])
        return gain_band*e.unitprice

    def node_gain(self, v: DataCenter) -> float:
        if len(v.requests) == 0:
            return 0
        multiplex_seq = [0 for _ in range(config.DURATION)]
        maxband = 0
        for r in v.requests:
            r: Request
            for i in range(config.DURATION):
                multiplex_seq[i] += r.bandSeq[i]
            maxband += r.bandwidth
        gain_band = sys.maxsize
        for i in range(config.DURATION):
            gain_band = min(gain_band, maxband-multiplex_seq[i])
        # print("maxband: {} gainband: {}".format(maxband, gain_band))
        return gain_band/maxband*v.cost

    def del_edgecount(self, pj: tuple, req:Request):
        e_ids = set()
        for i in range(len(pj)-1):
            e_ids.add((pj[i],pj[i+1]))
            e_ids.add((pj[i+1],pj[i]))
        for e in manager.edges.values():
            e: Edge
            if e.id not in e_ids:
                if req in e.requests:
                    e.requests.remove(req)
            else:
                e.requests.add(req)

    def del_node(self, pj: tuple, req:Request):
        target_node = -1
        for i in pj:
            if req in manager.nodes[i].requests:
                if target_node == -1 or len(manager.nodes[i].requests) >= len(manager.nodes[target_node].requests):
                    target_node = i
        for node in manager.nodes.values():
            if req in node.requests and node.id != target_node:
                node.requests.remove(req)
