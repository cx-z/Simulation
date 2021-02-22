#-*-coding:utf-8-*-
import os
from Shop import Shop

if __name__ == "__main__":
    os.system("clear")
    shop = Shop()
    profit1,profit2 = shop.sale()
    print("profit1 = " + str(profit1))
    print("profit2 = " + str(profit2))
