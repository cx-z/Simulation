#-*-coding:utf-8-*-
import heapq
import copy

import config
from Request import Request
from Caculator import Caculator
from Contrast import Contrast
from DataCenter import DataCenter
from Manager import manager
from VNF import VNF


class Shop:
    def __init__(self) -> None:
        super().__init__()
        self.profit1 = 0
        self.profit2 = 0
        self.caculator = Caculator()

    # 一个死循环的线程，负责接受用户的请求、计算是否接受请求以及请求的部署方案，并进行回复
    def sale(self)->float:
        req_offtime = list()
        req_ontime = copy.deepcopy(manager.requests)
        j = 0
        for i in range(config.DURATION):
            while len(req_offtime) and req_offtime[0].offtime >= i:
                req:Request = req_offtime[0]
                heapq.heappop(req_offtime)
            while req_ontime[j].ontime <= i:
                req:Request = req_ontime[j]
                if req.ontime < i:
                    break
                profit1 =  Caculator().calculate_profit(req)
                if profit1 > 0:
                    # print("req {}'s profit is {}".format(req.id, profit))
                    heapq.heappush(req_offtime, req)
                    self.profit1 += profit1
                profit2 = Contrast().calculate_profit(req)
                if profit2 > 0:
                    # print("req {}'s profit is {}".format(req.id, profit))
                    heapq.heappush(req_offtime, req)
                    self.profit2 += profit2
                j += 1
        return self.profit1, self.profit2
    