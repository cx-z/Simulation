#-*-coding:utf-8-*-

class VNF:
    def __init__(self, sfc_id:int,typ:int,seq:int,memory:int,cpu:float) -> None:
        super().__init__()
        self.sfc_id = sfc_id
        self.type = typ
        self.sequence = seq
        self.memory = memory
        self.unitDelayCpu = cpu
