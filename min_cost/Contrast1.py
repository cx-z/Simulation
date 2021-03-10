# -*-coding:utf-8 -*-
"""
本文件负责计算请求的部署节点以及利润
"""
import sys
import config

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


class Contrast1:
    def __init__(self) -> None:
        super().__init__()
        self.paths_pair = dict()  # <路径向量：Path实例>
        self.nodes = set()  # 最后得到的所需节点
        self.edges = set()  # 最后得到的所需链路<链路名：Edge实例>
        self.P_is = dict()  # 元素为req_id:P_i
        self.L_is = dict()  # 元素为req_id:L_i

    # 计算请求的利润和部署的节点
    # 如果利润不为正，部署节点为0
    def calculate_hardware(self) -> None:
        for req in manager.requests:
            self.choose_path(req)

        for node in self.nodes:
            node: DataCenter
            self.get_node_cost(node)
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
            node.cpu += r.process_source[node.id]
        node.cost = node.cpu * node.unitCpuPrice
        gain = self.node_gain(node)
        node.cpu *= (1 - gain / node.cost)
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
        edge.bandWidth *= (1 - gain / edge.cost)
        edge.cost -= gain

    # 判断是否存在环
    def has_circle(self, vec: tuple):
        points = set()
        for i in vec:
            if i not in points:
                points.add(i)
            else:
                return True
        return False

    def node_weight(self, req:Request, node:DataCenter):
        old_seq = [0 for _ in range(10)]
        for r in node.requests:
            r:Request
            for i in range(10):
                old_seq[i] += r.bandSeq[i]
        node.weight = (1-self.correlation(old_seq, req.bandSeq))/node.unitCpuPrice
        # node.weight = 1-self.correlation(old_seq, req.bandSeq)

    def path_weight(self, p:Path):
        p.weight = 0
        for e in p.edges:
            e:Edge
            p.weight -= e.unitprice

    # 返回目标路径
    def choose_path(self, req: Request):
        target_node:DataCenter = manager.nodes[0]
        target_node.weight = -1000
        k_paths = list()
        # g = Graph(False)
        # k_vecs = g.k_shortest_paths(req.src,req.dst,5)
        # for vec in list(k_vecs.keys()):
        #     if self.has_circle(vec):
        #         continue
        #     p: Path = Path(vec, 0)
        #     if p.propagation_delay < req.maxDelay:
        #         k_paths.append(p)
        if len(k_paths) == 0:
            k_vecs = Graph().k_shortest_paths(req.src,req.dst,2)
            for vec in k_vecs:
                p: Path = Path(vec[::-1], k_vecs[vec])
                if p.propagation_delay < req.maxDelay:
                    k_paths.append(p)
        target_path = k_paths[0]
        for p in k_paths:
            self.path_weight(p)
        for p in k_paths:
            p:Path
            if p.weight > target_path.weight:
                target_path = p
        for node in target_path.nodes:
            node: DataCenter
            self.node_weight(req, node)
            if node.weight >= target_node.weight:
                target_node = node
        self.check_constraints(req, target_path, target_node)
        target_node.requests.add(req)
        self.nodes.add(target_node)
        for e in target_path.edges:
            e:Edge
            e.requests.add(req)
            self.edges.add(e)

    def check_constraints(self, req: Request, path: Path, node: DataCenter) -> bool:
        # 检查时延
        if path.propagation_delay >= req.maxDelay:
            # print("req_id {} failed because delay".format(req.id))
            # print("maxDelay = {}, pdealy = {}".format(req.maxDelay, path.propagation_delay))
            return False
        # 处理时延
        process_delay = min(
            req.maxDelay - path.propagation_delay, len(req.sfc) * req.bandwidth)
        # 判断算力是否满足条件
        # 所需最低算力
        process_source = 0
        for vnf in req.sfc:
            process_source += config.VNF_DELAY[vnf]
        process_source *= 1 / process_delay
        # 判断是否有足够算力和最低算力开销
        # 没有可部署的节点，返回False
        req.process_source[node.id] = process_source
        req.path_vec.add(path.vec)
        return True

    def correlation(self, old_seq, new_seq) -> float:
        molecular: float = 0
        x = 0
        y = 0
        for i in range(len(old_seq)):
            molecular += old_seq[i] * new_seq[i]
            x += old_seq[i] * old_seq[i]
            y += new_seq[i] * new_seq[i]
        denominator: float = x ** 0.5 + y ** 0.5
        # if y == 0:
        #     print("old_seq is {}".format(old_seq))
        #     print("new_seq is {}".format(new_seq))
        return molecular / denominator

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
            gain_band = min(gain_band, maxband - multiplex_seq[i])
        return gain_band * e.unitprice

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
            gain_band = min(gain_band, maxband - multiplex_seq[i])
        # print("maxband: {} gainband: {}".format(maxband, gain_band))
        return gain_band / maxband * v.cost
