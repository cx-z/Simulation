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

cnt = 0
class Caculator:
    def __init__(self) -> None:
        super().__init__()
        self.paths_pair = dict()  # <路径向量：Path实例>
        self.nodes = dict()  # 最后得到的所需节点
        self.edges_pair = dict()  # 最后得到的所需链路<链路名：Edge实例>
        self.P_is = dict() # 元素为req_id:P_i
        self.L_is = dict()  # 元素为req_id:L_i

    # 计算请求的利润和部署的节点
    # 如果利润不为正，部署节点为0
    def calculate_hardware(self) -> None:
        for req in manager.requests:
            self.choose_path(req)
        print("{} qualified".format(cnt))
        paths = self.paths_pair.values()
        paths = list(paths)
        for p in paths:
            self.path_weight(p)
        paths = sorted(paths, key=lambda p: -p.weight)
        for p in paths:
            p: Path
            # print("{}'s weight is {}".format(p.vec, p.weight))
            for req_id in self.P_is:
                # print(len(P_i))
                P_i: set = self.P_is[req_id]
                if p.vec not in P_i or len(P_i) == 1:
                    continue
                for pj in P_i:
                    if pj != p.vec:
                        self.del_edgecount(pj, req_id)
                self.del_node(p.vec, req_id)
                P_i = {pj}
        for node in self.nodes.values():
            self.get_node_cost(node)
        for L_i in self.L_is.values():
            for e in L_i.values():
                e: Edge
                self.get_edge_cost(e)
                if e.id in self.edges_pair:
                    self.edges_pair[e.id].cost += e.cost
                    self.edges_pair[e.id].bandWidth += e.bandWidth
                else:
                    self.edges_pair[e.id] = e

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
        for L_i in self.L_is.values():
            if edge.id in L_i:
                edge.requests |= L_i[edge.id].requests
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
    def choose_path(self, req: Request) -> tuple:
        global cnt
        L_i = dict()
        P_i = set()
        for node in manager.nodes.values():
            node: DataCenter
            pre_half, pre_delay = Graph().get_shortest_path(req.src, node.id)
            pre_half = pre_half[::-1]
            second_half, second_delay = Graph().get_shortest_path(node.id, req.dst)
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
            node.cpu += req.process_source[node.id]
            if node.id not in self.nodes:
                self.nodes[node.id] = node
            P_i.add(path.vec)
            self.paths_pair[path_vec].bid += req.bid
            self.paths_pair[path_vec].band += req.bandwidth
            self.paths_pair[path_vec].requests.add(req)
            for p in P_i:
                # print("src = " + str(req.src) + " dst = "+ str(req.dst))
                # print("p: {}".format(str(p)))
                for e in self.paths_pair[p].edges:
                    e: Edge
                    if e.id in L_i:
                        L_i[e.id].usecount += 1
                    else:
                        L_i[e.id] = copy.deepcopy(e)
                        L_i[e.id].usecount = 1
                    L_i[e.id].requests = {req}
        # print("req_id: {},length of L_i: {}".format(req.id, len(L_i)))
        # print("req_id: {},length of P_i: {}".format(req.id, len(P_i)))
        if len(L_i) > 0:
            self.L_is[req.id]=L_i
        if len(P_i) > 0:
            self.P_is[req.id] = P_i
        cnt += 1

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
        path.weight = path.bid / (C_v + C_e)

    def check_constraints(self, req: Request, path: Path, node: DataCenter) -> bool:
        global cnt
        # 检查时延
        if path.propagation_delay >= req.maxDelay:
            # print("req_id {} failed because delay".format(req.id))
            # print("maxDelay = {}, pdealy = {}".format(req.maxDelay, path.propagation_delay))
            return False
        # 检查带宽费用是否亏本
        band_cost = 0
        for e in path.edges:
            e: Edge
            band_cost += e.unitprice*req.bandwidth
        if band_cost >= req.bid:
            # print("req_id {} failed because bandcost".format(req.id))
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
        profit: float = req.bid - band_cost - node.unitCpuPrice*process_source
        # 没有可部署的节点，返回False
        if profit > 0:
            req.process_source[node.id] = process_source
            # if req.id == 63:
            #     print("req63's node is {}".format(node.id))
            node.requests.add(req)
            node.cost += node.unitCpuPrice*req.process_source[node.id]
            for e in path.edges:
                e: Edge
                e.cost += req.bandwidth*e.unitprice
            return True
        else:
            # print("req_id {} failed because profit".format(req.id))
            return False

    def correlation(self, old_seq, new_seq) -> float:
        molecular: float = 0
        x = 0
        y = 0
        for i in len(old_seq):
            molecular += old_seq[i]*new_seq[i]
            x += old_seq[i]*old_seq[i]
            y += new_seq[i]*new_seq[i]
        denominator: float = x**0.5 + y**0.5
        return molecular/denominator

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

    def del_edgecount(self, pj: tuple, req_id:int):
        L_i: dict = self.L_is[req_id]
        for i in range(len(pj)-1):
            if (pj[i], pj[i+1]) not in L_i:
                continue
            if L_i[(pj[i], pj[i+1])].usecount > 1:
                L_i[(pj[i], pj[i+1])].usecount -= 1
            else:
                L_i.pop((pj[i], pj[i+1]))
        if len(L_i) == 0:
            del L_i
            print("{} 删完了".format(req_id))

    def del_node(self, pj: tuple, req_id:int):
        target_node = -1
        for r in manager.requests:
            if r.id != req_id:
                continue
            for i in pj:
                if r in self.nodes[i].requests:
                    if target_node == -1 or self.nodes[i].cost >= self.nodes[target_node].cost:
                        target_node = i
        for pj in self.P_is[req_id]:
            for i in pj:
                if r in self.nodes[i].requests and i != target_node:
                    if req_id == 34:
                        print(i)
                    self.nodes[i].requests.remove(r)
        # if target_node == -1:
        #     print("req{}'s targetnode is -1".format(req_id))
        # for i in pj:
        #     for r in self.paths_pair[pj].requests:
        #         r: Request
        #         if r in self.nodes[i].requests:
        #             self.nodes[i].cpu -= r.process_source[i]
        #             self.nodes[i].requests.remove(r)
        #         if self.nodes[i].cpu <= 0 or len(self.nodes[i].requests):
        #             print("节点{}不需要了".format(i))
        #             self.nodes.pop(i)
