#-*-coding:utf-8-*-


class Request:
    def __init__(self) -> None:
        super().__init__()
        self.id:int = 0
        self.src:str = ""
        self.dst:str = ""
        self.sfc:list = list() # sfc是一个列表，依次存储着每个vnf的类型
        self.bandwidth:int = 0
        self.bandSeq = list() # 流量大小序列
        self.bid:float = 0 # 此处的bid为单位时间的出价，因此计算总利润需要乘以offtime-ontime
        self.maxDelay:int = 0
        self.process_source = dict() # 存储在各个节点上所需的算力
        self.path_vec = set() # 路径集合
        self.node_id = -1

    def __lt__(self, other):
        if self.offtime < other.offtime:
            return True
        else:
            return False
