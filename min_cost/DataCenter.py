# -*-coding:utf-8-*-
"""
数据中心的类结构
"""


class DataCenter:
    def __init__(self, id: int, unitMemPrice: int, unitCpuPrice: int) -> None:
        super().__init__()
        self.id: int = id
        self.cpu: float = 0
        self.mem: float = 0
        self.unitMemprice: int = unitMemPrice
        self.unitCpuPrice: int = unitCpuPrice
        self.cost = 0
        self.neighbors = list()  # 此节点的邻接节点
        self.weight = 0
        self.requests = set()  # 当前在此节点运行的服务和复用增益<请求，增益>
        self.multiplexing_gain: float = 0
        self.discount:float = 0
