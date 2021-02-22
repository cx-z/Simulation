#-*-coding:utf-8-*-
"""
边的类结构
"""


class Edge:
    def __init__(self, endpoint1:int, endpoint2:int, bandwidth, unitprice) -> None:
        super().__init__()
        self.id = (endpoint1, endpoint2)
        self.propagationDelay:int = 0
        self.maxBand:int = bandwidth
        self.leftBand:int = bandwidth
        self.unitprice:int = unitprice
        self.charge:int = 0 # 指当前运行的服务的总收费
        self.requests = set() # 当前流量经过此链路的请求，以及该请求的增益<请求：增益>