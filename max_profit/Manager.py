# -*-coding:utf-8-*-
"""
本文件负责保存和修改所有请求、节点、链路等的信息
相当于一个数据中心
"""
from Singleton import Singleton

import config
from DataCenter import DataCenter
from Edge import Edge
from Request import Request


class Manager(metaclass = Singleton):
    def __init__(self) -> None:
        super().__init__()
        self.nodes: dict = dict() # 元素为 节点编号: DataCenter实例
        self.edges: dict = dict() # 元素为 "端点1 端点2": Edge实例
        self.requests: set = set() # 元素为 req.id:Request实例
        self.load_nodes_info()
        self.load_edges_info()

    # 从self.nodes中读取某节点的信息
    def load_nodes_info(self):
        for i in range(14):
            node = DataCenter(i,config.DataCenters[i],config.DataCenters[i])
            self.nodes[i] = node

    # 从self.edges中读取某链接的信息
    def load_edges_info(self):
        for key in config.Edge_UnitPrice:
            print(key)
            id = key
            e = Edge(id[0],id[1],0,config.Edge_UnitPrice[id])
            self.edges[id] = e
        for ed1 in config.GRAPH:
            for ed2 in config.GRAPH[ed1]:
                self.edges[(ed1,ed2)].propagationDelay = config.GRAPH[ed1][ed2]

    # 向self.requests中插入新上线的请求
    def insert_request_info(self, req: Request) -> None:
        self.requests[req.id] = req

    # 从self.requests中读取某个在线的请求信息
    def load_request_info(self, req_id: int) -> Request:
        return self.requests[req_id]

    # 从self.requests中删除下线的请求
    def del_request_info(self, req: Request) -> None:
        self.requests.pop(req.id)

manager = Manager()