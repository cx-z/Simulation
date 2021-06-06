#-*-coding:utf-8-*-


class Request:
    def __init__(self) -> None:
        super().__init__()
        self.id:int = 0
        self.src:int = -1
        self.dst:int = -1
        self.sfc:list = list() # sfc是一个列表，依次存储着每个vnf的类型
        self.bandwidth:int = 0
        self.bid:float = 0 # 此处的bid为单位时间的出价，因此计算总利润需要乘以offtime-ontime
        self.unitBid:float = 0
        self.ontime:int = -1
        self.offtime:int = -1
        self.maxDelay:int = 0
        self.process_source = dict() # 存储在各个节点上所需的算力
        self.path_vec = tuple() # 路径集合
        self.node_id = -1

    def __lt__(self, other):
        if self.offtime < other.offtime:
            return True
        else:
            return False
