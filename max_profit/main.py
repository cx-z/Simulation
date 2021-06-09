#-*-coding:utf-8-*-
import os
from Shop import Shop
import createData
from Manager import manager
import matplotlib.pyplot as plt
import time

def swap(x,y):
    t = x
    x = y
    y = t

if __name__ == "__main__":
    os.system("clear")
    r11 = []
    r12 = []
    r21 = []
    r22 = []
    r31 = []
    r32 = []
    t1 = []
    t2 = []
    t3 = []
    x = []
    for j in range(10):
        x.append((j+1)*100)
        createData.req_info(x[-1])
        print("{} requests".format(len(manager.requests)))
        for i in range(3):
            manager.requests.clear()
            manager.edges.clear()
            manager.nodes.clear()
            manager.load_requests_info()
            manager.load_edges_info()
            manager.load_nodes_info()
            shop = Shop(i)
            start = time.time()
            profit,req_num = shop.sale()
            end = time.time()
            print("Algorithm {}： profit is {} and accept num is {}".format(i,profit,req_num))
            if i == 0:
                r11.append(req_num/x[-1])
                r12.append(profit)
                t1.append(end-start)
            elif i == 1:
                r21.append(req_num/x[-1])
                r22.append(profit)
                t2.append(end-start)
            else:
                r31.append(req_num/x[-1])
                r32.append(profit)
                t3.append(end-start)
    
    plt.rcParams['font.sans-serif'] = ['SimSun']  # 用来正常显示中文标签
    p1 = plt.plot(x,r11,marker='+')
    plt.plot(x, r21, marker='d')
    plt.plot(x, r31, marker='s')
    plt.legend(('GDWP','OLPM','greedy'),loc='upper right')
    plt.xlabel('SFC 数（个）', fontsize=15)
    plt.ylabel('请求接受率', fontsize=15)
    plt.ylim(0,1)
    plt.show()
    p2 = plt.plot(x, r12, marker='+')
    plt.plot(x, r22, marker='d')
    plt.plot(x, r32, marker='s')
    plt.legend(('GDWP', 'OLPM', 'greedy'), loc='upper left')
    plt.xlabel('SFC 数（个）', fontsize=15)
    plt.ylabel('总利润', fontsize=15)
    plt.show()
    print(t1)
    print(t2)
    print(t3)
    p4 = plt.plot(x, t1, marker='+')
    plt.plot(x, t2, marker='d')
    plt.plot(x, t3, marker='s')
    plt.legend(('GDWP', 'OLPM', 'greedy'), loc='upper left')
    plt.xlabel('SFC 数（个）', fontsize=15)
    plt.ylabel('计算时间（秒）', fontsize=15)
    plt.show()
