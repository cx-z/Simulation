#-*-coding:utf-8-*-
from Edge import Edge
import config
import sys
from Request import Request
from DataCenter import DataCenter
from Manager import manager
from Caculator import Caculator
from Contrast2 import Contrast2
from Contrast1 import Contrast1


class Shop:
    def __init__(self, i) -> None:
        super().__init__()
        self.profit = 0
        self.requests = list()
        self.edges = list() # 需要购买的链路
        self.nodes = list() # 需要购买的数据中心
        if i == 0:
            self.caculator = Caculator()
        elif i == 1:
            self.caculator = Contrast1()
        else:
            self.caculator = Contrast2()

    # 一个死循环的线程，负责接受用户的请求、计算是否接受请求以及请求的部署方案，并进行回复
    def sale(self)->float and int and int and float:
        self.input_requests()
        return self.caculate_cost(),len(self.caculator.nodes),len(self.caculator.edges)

    # 从文件中读取请求
    def input_requests(self)->None:
        bid = 0
        f = open("requests.txt")
        lines = f.readlines()
        i = 0
        while i < len(lines):
            # 每个请求写成两行，第一行为除序列外其他信息
            line = lines[i].split(" ")
            # print(line)
            req = Request()
            req.id = int(line[0])
            req.src = int(line[1])
            req.dst = int(line[2])
            req.bandwidth = int(line[3])
            bid += req.bid
            req.maxDelay = int(line[4])
            req.sfc = line[5:-1]
            # 第二行为流量序列
            seq = lines[i+1].split(" ")
            for j in range(len(seq)-1):
                req.bandSeq.append(int(seq[j]))
            manager.requests.add(req)
            i += 2

    def link_concentration(self)->float:
        costs = []
        total_cost = 0
        for e in self.caculator.edges:
            e:Edge
            costs.append(e.cost)
            total_cost += e.cost
        costs.sort(reverse=True)
        head = 0
        for i in range(5):
            head += costs[i]
        return head/total_cost
            
    # 调用类Caculator的calculate_profit函数计算利润和应部署的节点
    # 此函数计算完利润后，需要修改req的属性，包括req.sfc里各个VNF的属性
    def caculate_cost(self)->float:
        cost = 0
        self.caculator.calculate_hardware()
        max_node_cpu = 0
        for node in self.caculator.nodes:
            node:DataCenter
            max_node_cpu = max(max_node_cpu,node.cpu)
        for node in self.caculator.nodes:
            # print("node {} has {} requests".format(node.id,len(node.requests)))
            cost += node.cost*self.node_discount(node)
        print("max_node_cpu" + str(max_node_cpu))
        max_edge_band = 0
        for edge in self.caculator.edges:
            edge:Edge
            max_edge_band = max(max_edge_band,edge.bandWidth)
        for edge in self.caculator.edges:
            # print("edge {} has {} requests".format(edge.id, len(edge.requests)))
            cost += edge.cost*self.edge_discount(edge)
        print("max_edge_band" + str(max_edge_band))
        return cost

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