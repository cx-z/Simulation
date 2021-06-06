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
        # paths = list(paths)
        for p in paths:
            p: Path
            self.path_weight(p)
        # paths = sorted(paths, key=lambda p: -p.weight)
        for node in manager.nodes.values():
            node: DataCenter
            node.requests.clear()
        for edge in manager.edges.values():
            edge: Edge
            edge.requests.clear()
        for r in manager.requests:
            r: Request
            self.del_redundant_path(r)
        num = 0
        for node in manager.nodes.values():
            node: DataCenter
            if len(node.requests) > 0:
                num += len(node.requests)
                self.nodes.add(node)
                self.get_node_cost(node)
        print("nodes deploy {} requests".format(num))
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
            node.cpu += r.process_source
            # print("node {} deploy req {} needs cpu {}".format(node.id,r.id, r.process_source[node.id]))
        node.cost = node.cpu * node.unitCpuPrice
        gain = self.node_gain(node)
        node.gain = gain
        node.cpu *= (1-gain/node.cost)
        node.cost -= gain
        node.cost *= 0.9

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
        edge.gain = gain
        edge.bandWidth *= (1-gain/edge.cost)
        edge.cost -= gain
        edge.cost *= 0.9

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
                req.path_vec.add(path_vec)
            else:
                path: Path = self.paths_pair[path_vec]
                if not self.check_constraints(req, path, node):
                    continue

    # 计算每条可用路径的选择权重
    def path_weight(self, path: Path) -> None:
        C_v: float = 0
        v_gain = 0
        e_gain = 0
        price = 0
        for v in path.nodes:
            v: DataCenter
            self.get_node_cost(v)
            C_v += v_gain / (self.node_discount(v)*v.unitCpuPrice*v.unitCpuPrice*v.cpu)
            # print("{} {}".format(v.cpu, self.node_discount(v)))
        C_e = 0
        for e in path.edges:
            e: Edge
            self.get_edge_cost(e)
            C_e += e_gain / (self.edge_discount(e)*e.unitprice*e.unitprice*e.bandWidth)
            price += e.unitprice
        path.weight = (C_e + C_v)/price

    def node_weight(self, v: DataCenter):
        # v.weight = v.gain/(self.node_discount(v)*v.unitCpuPrice*v.unitCpuPrice*v.cpu)
        v.weight =  1/ v.unitCpuPrice

    def check_constraints(self, req: Request, path: Path, node: DataCenter) -> bool:
        # 检查时延
        if path.propagation_delay >= req.maxDelay:
            # print("req_id {} failed because delay".format(req.id))
            # print("maxDelay = {}, pdealy = {}".format(req.maxDelay, path.propagation_delay))
            return False
        # print("----------------")
        # print((req.maxDelay - path.propagation_delay)/1000)
        # print(len(req.sfc)/req.bandwidth)
        # print("----------------")
        # 判断算力是否满足条件
        # 所需最低算力
        if req.process_source <= 0:
            for vnf in req.sfc:
                req.process_source += config.VNF_DELAY[vnf]
            req.process_source *= req.bandwidth
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
        e.bandWidth = maxband-gain_band
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
        return gain_band*v.unitCpuPrice

    def del_redundant_path(self, req: Request):
        target_vec = list(req.path_vec)[0]
        for vec in req.path_vec:
            if self.paths_pair[vec].weight > self.paths_pair[target_vec].weight:
                target_vec = vec
        target_v: DataCenter = self.paths_pair[target_vec].nodes[0]
        for v in self.paths_pair[target_vec].nodes:
            v: DataCenter
            self.node_weight(v)
            if v.weight > target_v.weight:
                target_v = v
        target_v.requests.add(req)
        for e in self.paths_pair[target_vec].edges:
            e: Edge
            e.requests.add(req)
        req.path_vec.clear()
        req.path_vec.add(target_vec)

    def edge_discount(self, edge:Edge)->float:
        keys = config.Edge_Discount.keys()
        keys = list(keys)
        keys.sort()
        if edge.bandWidth >= config.Edge_Discount[keys[3]]:
            return config.Edge_Discount[keys[3]]
        elif edge.bandWidth >= config.Edge_Discount[keys[2]]:
            return config.Edge_Discount[keys[2]]
        elif edge.bandWidth >= config.Edge_Discount[keys[1]]:
            return config.Edge_Discount[keys[1]]
        elif edge.bandWidth >= config.Edge_Discount[keys[0]]:
            return config.Edge_Discount[keys[0]]
        else:
            return 1

    def node_discount(self,node:DataCenter)->float:
        keys = config.Node_Discount.keys()
        keys = list(keys)
        keys.sort()
        if node.cpu >= keys[3]:
            return config.Node_Discount[keys[3]]
        elif node.cpu >= keys[2]:
            return config.Node_Discount[keys[2]]
        elif node.cpu >= keys[1]:
            return config.Node_Discount[keys[1]]
        elif node.cpu >= keys[0]:
            return config.Node_Discount[keys[0]]
        else:
            return 1