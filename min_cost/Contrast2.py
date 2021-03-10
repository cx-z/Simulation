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
        for node in self.nodes:
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
        _,path_vec, delay = Graph().get_shortest_path(req.src, req.dst)
        path_vec = path_vec[::-1]
        node_id = path_vec[0]
        for i in path_vec:
            if manager.nodes[node_id].unitCpuPrice > manager.nodes[i].unitCpuPrice:
                node_id = i
        node:DataCenter = manager.nodes[node_id]
        path = Path(path_vec, delay)
        self.check_constraints(req,path,node)
        node.requests.add(req)
        self.nodes.add(node)
        for i in range(len(path_vec)-1):
            e: Edge = manager.edges[(path_vec[i],path_vec[i+1])]
            e.requests.add(req)
            self.edges.add(e)

    def check_constraints(self, req: Request, path: Path, node: DataCenter) -> bool:
        # 检查时延
        if path.propagation_delay >= req.maxDelay:
            print("req_id {} failed because delay".format(req.id))
            print("maxDelay = {}, pdealy = {}".format(req.maxDelay, path.propagation_delay))
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
        # 判断是否有足够算力和最低算力开销
        req.process_source[node.id] = process_source
        node.requests.add(req)
        for e in path.edges:
            e: Edge
            e.requests.add(req)
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
