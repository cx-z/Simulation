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


class Contrast2:
    def __init__(self) -> None:
        super().__init__()
        self.nodes = set()  # 最后得到的所需节点
        self.edges = set()  # 最后得到的所需链路<链路名：Edge实例>

    # 计算请求的利润和部署的节点
    # 如果利润不为正，部署节点为0
    def calculate_hardware(self) -> None:
        for req in manager.requests:
            self.choose_path(req)
        num = 0
        for node in self.nodes:
            num += len(node.requests)
            self.get_node_cost(node)
        print("nodes deploy {} requests".format(num))
        for e in self.edges:
            e: Edge
            self.get_edge_cost(e)

    def get_node_cost(self, node: DataCenter):
        node.cpu = 0
        node.cost = 0
        if len(node.requests) == 0:
            return
        for r in node.requests:
            r: Request
            node.cpu += r.process_source
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
        paths_pair = dict() # key:value  路径向量：路径对象
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
            if path_vec not in paths_pair:
                path = Path(path_vec, pre_delay + second_delay)
                if not self.check_constraints(req, path, node):
                    continue
                paths_pair[path_vec] = path
        target_path: Path = list(paths_pair.values())[0]
        for p in paths_pair.values():
            p: Path
            if p.weight > target_path.weight:
                target_path = p
        for e in target_path.edges:
            e: Edge
            e.requests.add(req)
            self.edges.add(e)
        target_v: DataCenter = target_path.nodes[0]
        for v in target_path.nodes:
            v: DataCenter
            if v.unitCpuPrice < target_v.unitCpuPrice:
                target_v = v
        target_v.requests.add(req)
        self.nodes.add(target_v)

    def check_constraints(self, req: Request, path: Path, node: DataCenter) -> bool:
        # 检查时延
        if path.propagation_delay >= req.maxDelay:
            # print("req_id {} failed because delay".format(req.id))
            # print("maxDelay = {}, pdealy = {}".format(req.maxDelay, path.propagation_delay))
            return False
        # 所需最低算力
        # print("+++++++++++++++")
        # print((req.maxDelay - path.propagation_delay) / 1000)
        # print(len(req.sfc) / req.bandwidth)
        # print("+++++++++++++++")
        process_source = 0
        for vnf in req.sfc:
            process_source += config.VNF_DELAY[vnf]
        process_source *= req.bandwidth
        # 判断是否有足够算力和最低算力开销
        req.process_source = process_source
        path.weight = node.unitCpuPrice * req.process_source
        for e in path.edges:
            e: Edge
            path.weight += e.unitprice*req.bandwidth
        path.weight = 1/path.weight
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
        return gain_band*v.unitCpuPrice
