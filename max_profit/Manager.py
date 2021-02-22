# -*-coding:utf-8-*-
"""
本文件负责保存和修改所有请求、节点、链路等的信息
相当于一个数据中心
"""
import heapq

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
        self.requests: list = list() # 元素为 req.id:Request实例
        self.load_nodes_info()
        self.load_edges_info()
        self.load_requests_info()

    # 从self.nodes中读取某节点的信息
    def load_nodes_info(self):
        for i in range(14):
            node = DataCenter(i,config.DataCenters_Price[i],config.DataCenters_CPU[i])
            self.nodes[i] = node

    # 从self.edges中读取某链接的信息
    def load_edges_info(self):
        for key in config.Edge_UnitPrice:
            id = key
            e = Edge(id[0],id[1],0,config.Edge_UnitPrice[id])
            self.edges[id] = e
        for ed1 in config.GRAPH:
            for ed2 in config.GRAPH[ed1]:
                self.edges[(ed1,ed2)].propagationDelay = config.GRAPH[ed1][ed2]
                self.edges[(ed1,ed2)].maxBand = config.Edge_Band[(ed1,ed2)]
                self.edges[(ed1,ed2)].leftBand = config.Edge_Band[(ed1,ed2)]

    def load_requests_info(self):
        f = open("requests.txt")
        lines = f.readlines()
        for i in range(len(lines)):
            # 每个请求写成两行，第一行为除序列外其他信息
            line = lines[i].split(" ")
            # print(line)
            req = Request()
            req.id = int(line[0])
            req.src = int(line[1])
            req.dst = int(line[2])
            req.bandwidth = int(line[3])
            req.bid = int(line[4])
            req.maxDelay = int(line[5])
            req.ontime = int(line[6])
            req.offtime = int(line[7])
            req.unitBid = req.bid / (req.offtime - req.ontime)
            req.sfc = line[8:-1]
            self.requests.append(req)
        self.requests = sorted(self.requests, key=lambda r: r.ontime)

    def del_requests(self, req:Request):
        for i in range(len(req.path_vec)-1):
            e:Edge = self.edges[(req.path_vec[i],req.path_vec[i+1])]
            self.edge_del_req(e,req)
            e:Edge = self.edges[(req.path_vec[i+1],req.path_vec[i])]
            self.edge_del_req(e,req)
        self.node_del_req(req.node_id, req)

    def add_requests(self, req:Request):
        for i in range(len(req.path_vec)-1):
            e:Edge = self.edges[(req.path_vec[i],req.path_vec[i+1])]
            self.edge_add_req(e,req)
            e:Edge = self.edges[(req.path_vec[i+1],req.path_vec[i])]
            self.edge_add_req(e,req)
        self.node_add_req(req.node_id, req)

    def node_add_req(self, node_id:int, req:Request):
        self.nodes[node_id].leftCpu -= req.process_source[node_id]
        self.nodes[node_id].charge += req.bid

    def node_del_req(self, node_id:int, req:Request):
        self.nodes[node_id].leftCpu += req.process_source[node_id]
        self.nodes[node_id].charge -= req.bid

    def edge_add_req(self, edge:Edge, req:Request):
        edge.leftBand -= req.bandwidth
        edge.charge += req.bid/len(req.path_vec)
    
    def edge_del_req(self, edge:Edge, req:Request):
        edge.leftBand += req.bandwidth
        edge.charge -= req.bid/len(req.path_vec)

manager = Manager()