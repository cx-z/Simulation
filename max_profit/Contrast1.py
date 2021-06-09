# -*-coding:utf-8 -*-
"""
本文件负责计算请求的部署节点以及利润
"""
import config

from Manager import manager
from DataCenter import DataCenter
from Request import Request
from Edge import Edge
from Graph import Graph
from Path import Path


def cmp(x, y):
    if x<y:
        return -1
    elif x==y:
        return 0
    else:
        return 1

class Contrast1:
    def __init__(self) -> None:
        super().__init__()
        
    # 计算请求的利润和部署的节点
    # 如果利润不为正，部署节点为0
    def calculate_profit(self,req:Request)->float:
        path:Path = self.choose_path(req)
        if not path:
            return 0
        node:DataCenter = self.choose_node(req, path)
        for e in path.edges:
            e:Edge
            e.leftBand -= req.bandwidth
        return req.profit

    # 返回目标路径
    def choose_path(self,req:Request)->Path:
        k_paths = dict() # 元素为<路径向量，传播时延>
        graph = Graph()
        for node in manager.nodes.values():
            node: DataCenter
            _,pre_half, pre_delay = graph.get_shortest_path(req.src, node.id)
            pre_half = pre_half[::-1]
            _,second_half, second_delay = graph.get_shortest_path(node.id, req.dst)
            second_half = second_half[::-1]
            path_vec = pre_half + second_half[1:]
            path_vec = tuple(path_vec)
            if self.has_circle(path_vec) or pre_delay+second_delay>=req.maxDelay:
                continue
            # print("src = " + str(req.src) + " dst = "+ str(req.dst))
            k_paths[path_vec] = pre_delay+second_delay
        # print("req {} has {} alternative pathes".format(req.id, len(k_paths)))
        paths = list()
        for p in k_paths:
            path:Path = Path(p, k_paths[p])
            if self.check_constraints(req, path):
                paths.append(path)
        if len(paths) == 0:
            return None
        target_path:Path = paths[0]
        for p in paths:
            p:Path
            if p.greedy_profit > target_path.greedy_profit:
                target_path = p
        req.path_vec = target_path.vec
        return target_path
        
    # 判断是否存在环
    def has_circle(self, vec:tuple):
        points = set()
        for i in vec:
            if i not in points:
                points.add(i)
            else:
                return True
        return False

    # 计算每条可用路径的选择权重
    def path_weight(self, req:Request, path:Path)->None:
        # path的最后两项是带宽成本和贪心利润
        path.weight = path.greedy_profit # 贪心利润

    # 从目标路径中选择部署节点
    # 此处输入的path最后三项依次是band_cost、greedy_profit和路径权重
    def choose_node(self,req:Request, path:Path)->DataCenter:
        # 首先计算部署在每个节点上的利润
        for node in path.nodes:
            node:DataCenter
            if node.leftCpu < req.process_source:
                node.weight = -1
            else:
                node.weight = node.unitCpuPrice
        target_node:DataCenter = path.nodes[0]
        for node in path.nodes:
            if node.weight > target_node.weight:
                target_node = node
        req.profit = (req.bid/(req.offtime-req.ontime) - path.band_cost - target_node.unitCpuPrice*req.process_source)*(req.offtime-req.ontime)
        target_node.leftCpu -= req.process_source
        req.node_id = target_node.id
        return target_node

    def check_constraints(self,req:Request, path:Path)->bool:
        if path.greedy_profit >  0:
            return True
        # 检查时延
        if path.propagation_delay >= req.maxDelay:
            # print("req {} and {} failed because of delay".format(req.id, path.vec))
            return False
        # 检查带宽和带宽费用
        for e in path.edges:
            e:Edge
            if e.leftBand < req.bandwidth:
                # print("req {} and {} failed because of band".format(req.id, path.vec))
                # print("req {}'s band is {}".format(req.id,req.bandwidth))
                # print("edge {}'s band is {}".format(e.id,e.leftBand))
                return False
            path.band_cost += e.unitprice*req.bandwidth
        if path.band_cost >= req.bid/(req.offtime-req.ontime):
            # print("req {} and {} failed because of band_cost".format(req.id, path.vec))
            return False
        # 处理时延
        if req.maxDelay - path.propagation_delay  - len(req.sfc)*1000/req.bandwidth< 0:
            # print("req {} and {} failed because of delay".format(req.id, path.vec))
            return False
        # 判断算力是否满足条件
        # 所需最低算力
        if req.process_source <= 0:
            for vnf in req.sfc:
                req.process_source += config.VNF_DELAY[vnf]
            req.process_source *= req.bandwidth
        # 判断是否有足够算力和最低算力开销
        for node in path.nodes:
            node:DataCenter
            # 判断节点剩余算力是否足够部署sfc
            if node.leftCpu < req.process_source:
                # print("req {} and {} failed because of cpu".format(req.id, node.id))
                continue
            # 判断在该节点部署SFC是否亏本
            profit = req.bid/(req.offtime-req.ontime) - path.band_cost - node.unitCpuPrice*req.process_source
            if profit <= 0:
                # print("req {} and {} failed because of profit".format(req.id, path.vec))
                continue
            # 上述两个条件都满足，表示可以在该路径部署，计算或更新贪心利润
            path.greedy_profit = max(profit, path.greedy_profit)
        # 没有可部署的节点，返回False
        return path.greedy_profit > 0
