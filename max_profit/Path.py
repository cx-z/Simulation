#-*-coding:utf-8-*-

import sys

from DataCenter import DataCenter
from Edge import Edge
from Manager import manager


class Path:
    def __init__(self, path_vec:tuple, delay:int) -> None:
        super().__init__()
        self.vec = path_vec # 存储路径上各个节点id的元组
        self.nodes = list()
        self.edges = list()
        self.requests = set()
        self.band:int = 0
        self.band_cost:float = 0
        self.cost:float = 0
        self.propagation_delay:int = delay
        self.process_delay:int = sys.maxsize
        self.process_source:float = 0
        self.greedy_profit:float = 0
        self.bid:float = 0
        self.weight:float = 0 # 路径选择权重
        self.profit = 0 # 选定路径和节点后，最终的利润
        self.init_edges(path_vec)
        self.init_nodes(path_vec)
        
    def init_nodes(self, path:tuple):
        for v in path:
            node = manager.nodes[v]
            self.nodes.append(node)

    def init_edges(self, path:tuple):
        for i in range(len(path)-1):
            e = manager.edges[(path[i],path[i+1])]
            self.edges.append(e)

