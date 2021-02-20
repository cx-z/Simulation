# -*-coding:utf-8 -*-
"""
拓扑图
"""
import heapq
import sys
import copy

import config
from DataCenter import DataCenter
from Manager import Manager


class Graph(object):
    def __init__(self) -> None:
        super().__init__()
        self.graph = config.GRAPH # 元素结构为 node:{node:[weight,bandwidth],...}

    def get_shortest_path(self, start, end) -> int and list and int:
        # distances使用字典的方式保存每一个顶点到startpoint点的距离
        distances = {}
        # 从startpoint到某点的最优路径的前一个结点
        # eg:startpoint->B->D->E,则previous[E]=D,previous[D]=B,等等
        previous = {}
        # 用来保存图中所有顶点的到startpoint点的距离的优先队列
        # 这个距离不一定是最短距离
        nodes = []
        # Dikstra算法 数据初始化
        for vertex in self.graph:
            if vertex == start:
                # 将startpoint点的距离初始化为0
                distances[vertex] = 0
                heapq.heappush(nodes, [0, vertex])
            elif vertex in self.graph[start]:
                # 把与startpoint点相连的结点距离startpoint点的距离初始化为对应的弧长/路权
                distances[vertex] = self.graph[start][vertex]
                heapq.heappush(nodes, [self.graph[start][vertex], vertex])
                previous[vertex] = start
            else:
                # 把与startpoint点不直接连接的结点距离startpoint的距离初始化为sys.maxsize
                distances[vertex] = sys.maxsize
                heapq.heappush(nodes, [sys.maxsize, vertex])
                previous[vertex] = None

        shortest_path = []
        lenPath = sys.maxsize
        while nodes:
            # 取出队列中最小距离的结点
            smallest = heapq.heappop(nodes)[1]
            if smallest == end:
                shortest_path = []
                lenPath = distances[smallest]
                temp = smallest
                while temp != start:
                    shortest_path.append(temp)
                    temp = previous[temp]
                # 将startpoint点也加入到shortest_path中
                shortest_path.append(temp)
            if distances[smallest] == sys.maxsize:
                # 所有点不可达
                break
            # 遍历与smallest相连的结点，更新其与结点的距离、前继节点
            for neighbor in self.graph[smallest]:
                dis = distances[smallest] + self.graph[smallest][neighbor]
                if dis < distances[neighbor]:
                    distances[neighbor] = dis
                    # 更新与smallest相连的结点的前继节点
                    previous[neighbor] = smallest
                    for node in nodes:
                        if node[1] == neighbor:
                            # 更新与smallest相连的结点到startpoint的距离
                            node[0] = dis
                            break
                    heapq.heapify(nodes)
        return shortest_path, lenPath
