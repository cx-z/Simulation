# -*-coding:utf-8-*-
"""
数据中心的类结构
"""


class DataCenter:
    def __init__(self, id: int, unitCpuPrice: int, cpu:float) -> None:
        super().__init__()
        self.id: int = id
        self.maxCpu: float = cpu
        self.leftCpu: float = cpu
        self.mem: float = 0
        # self.unitMemprice: int = unitMemPrice
        self.unitCpuPrice: int = unitCpuPrice
        self.charge = 0
        self.neighbors = list()  # 此节点的邻接节点
        self.weight = 0
        self.requests = list()  # 当前在此节点运行的服务
