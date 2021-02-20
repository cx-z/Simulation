#-*-coding:utf-8-*-
from Manager import manager
import os
from Request import Request
from Shop import Shop

if __name__ == "__main__":
    os.system("clear")
    shop = Shop()
    cost = shop.sale()
    print("cost = " + str(cost))
