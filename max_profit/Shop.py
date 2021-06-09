#-*-coding:utf-8-*-
import heapq
import copy

import config
from Request import Request
from Caculator import Caculator
from Contrast1 import Contrast1
from Contrast2 import Contrast2
from DataCenter import DataCenter
from Manager import manager


class Shop:
    def __init__(self, choice:int) -> None:
        super().__init__()
        self.profit:float = 0
        self.req_num:float = 0
        if choice == 0:
            self.caculator = Caculator()
        elif choice == 1:
            self.caculator = Contrast1()
        else:
            self.caculator = Contrast2()

    # 一个死循环的线程，负责接受用户的请求、计算是否接受请求以及请求的部署方案，并进行回复
    def sale(self)->float and int:

        for req in manager.requests:
            profit = self.caculator.calculate_profit(req)
            if profit > 0:
                self.profit += profit
                self.req_num += 1
        # j = 0
        # for i in range(config.DURATION):
        #     while len(req_offtime) and req_offtime[0].offtime >= i:
        #         # req:Request = req_offtime[0]
        #         heapq.heappop(req_offtime)
        #     while req_ontime[j].ontime <= i:
        #         req: Request = req_ontime[j]
        #         if req.ontime < i:
        #             break
        #         profit = self.caculator.calculate_profit(req)
        #         if profit > 0:
        #             # print("req {}'s profit is {}".format(req.id, profit))
        #             heapq.heappush(req_offtime, req)
        #             self.profit += profit
        #             self.req_num += 1
        #         j += 1
        return self.profit, self.req_num
    