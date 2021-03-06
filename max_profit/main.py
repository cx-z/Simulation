#-*-coding:utf-8-*-
from Manager import manager
import os
from Request import Request
from Shop import Shop

if __name__ == "__main__":
    os.system("clear")
    shop = Shop()
    cost1,cost2 = shop.sale()
    print("cost1 = " + str(cost1))
    print("cost2 = " + str(cost2))
