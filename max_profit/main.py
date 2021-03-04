#-*-coding:utf-8-*-
import os
from Shop import Shop
import createData
from Manager import manager

if __name__ == "__main__":
    os.system("clear")
    createData.req_info(1000)
    manager.load_requests_info()
    for i in range(3):
        shop = Shop(i)
        profit,req_num = shop.sale()
        print("Algorithm {}： profit is {} and accept num is {}".format(i,profit,req_num))
