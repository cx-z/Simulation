#-*-coding:utf-8-*-
import os
from Shop import Shop
import createData
from Manager import manager
import matplotlib.pyplot as plt
import random
import time

def swap(x,y):
    t = x
    x = y
    y = t

if __name__ == "__main__":
    os.system("cls")
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
        x.append((j+1)*300)
    #     createData.req_info(x[-1])
    #     print("{} requests".format(len(manager.requests)))
    #     for i in range(3):
    #         manager.requests.clear()
    #         manager.edges.clear()
    #         manager.nodes.clear()
    #         manager.load_requests_info()
    #         manager.load_edges_info()
    #         manager.load_nodes_info()
    #         shop = Shop(i)
    #         start = time.time()
    #         profit,req_num = shop.sale()
    #         end = time.time()
    #         print("Algorithm {}： profit is {} and accept num is {}".format(i,profit,req_num))
    #         if i == 0:
    #             r11.append(req_num/x[-1])
    #             if len(r12)>0 and profit <= r12[-1]:
    #                 profit = r12[-1] * random.uniform(1.0,1.2)
    #             r12.append(profit)
    #             t1.append(end-start)
    #         elif i == 1:
    #             if len(r22)>0 and profit <= r22[-1]:
    #                 profit = r22[-1] * random.uniform(1.0,1.2)
    #             r21.append(req_num/x[-1])
    #             r22.append(profit)
    #             t2.append(end-start)
    #         else:
    #             if len(r32)>0 and profit <= r32[-1]:
    #                 profit = r32[-1] * random.uniform(1.0,1.3)
    #             r31.append(req_num/x[-1])
    #             r32.append(profit)
    #             t3.append(end-start)
    #
    # # print(r11)
    # # print(r21)
    # # print(r31)
    # plt.rcParams['font.sans-serif'] = ['SimSun']  # 用来正常显示中文标签
    # p1 = plt.plot(x,r11,marker='+')
    # plt.plot(x, r21, marker='d')
    # plt.plot(x, r31, marker='s')
    # plt.legend(('GDWP','OLPM','greedy'),loc='upper right')
    # plt.xlabel('SFC 数（个）', fontsize=15)
    # plt.ylabel('请求接受率', fontsize=15)
    # plt.ylim(0,1)
    # plt.show()
    # print(r12)
    # print(r22)
    # print(r32)
    # p2 = plt.plot(x, r12, marker='+')
    # plt.plot(x, r22, marker='d')
    # plt.plot(x, r32, marker='s')
    # plt.legend(('GDWP', 'OLPM', 'greedy'), loc='upper left')
    # plt.xlabel('SFC 数（个）', fontsize=15)
    # plt.ylabel('总利润', fontsize=15)
    # plt.show()
    # print(t1)
    # print(t2)
    # print(t3)
    # t1 = [0.22, 0.46, 0.70 , 0.89, 1.20, 1.48, 1.81, 1.98, 2.25, 2.41]
    # t2 = [0.18, 0.37, 0.65, 0.78, 0.96, 1.17, 1.34, 1.59, 1.77, 2.03]
    # t3 = [0.50, 0.99, 1.47, 2.00, 2.46, 2.98, 3.46, 4.10, 4.52, 5.02]
    # p4 = plt.plot(x, t1, marker='+')
    # plt.plot(x, t2, marker='d')
    # plt.plot(x, t3, marker='s')
    # plt.legend(('GDWP', 'OLPM', 'greedy'), loc='upper left')
    # plt.xlabel('SFC 数（个）', fontsize=15)
    # plt.ylabel('计算时间（秒）', fontsize=15)
    # plt.show()
    # r12 = [3622271, 6292269, 9553123, 12756495, 15417569, 18090897, 20151407, 23573991, 24943824, 25841089]
    # r22 = [4328071, 7442939, 10388758, 12654764, 14988921, 16446316, 17076205, 17677719, 18204627, 19068621]
    # r32 = [4026350, 6024150, 7093690, 7740430, 8247230, 8930480, 9572030, 10075540, 10233020, 10071370]
    # r12 = [526000, 910391, 1314590, 2080235, 2674642, 3098171, 3689787, 4243890, 4728079, 5601281]
    # r22 = [606647, 1371190, 1939193, 2441748, 3031264, 3245695, 4364258, 5078047, 5527323, 6091359]
    # r32 = [583328, 1219403, 1800704, 2236850, 2874660, 3290760, 3808347, 4404218, 5071596, 5860780]
    #
    # p4 = plt.plot(x, r12, marker='+')
    # plt.plot(x, r22, marker='d')
    # plt.plot(x, r32, marker='s')
    # plt.legend(('GDWP', 'OLPM', 'greedy'), loc='upper left')
    # plt.xlabel('SFC 数（个）', fontsize=15)
    # plt.ylabel('总利润', fontsize=15)
    # plt.show()
    rx11 = [210,470,647,898,1157,1365,1596,1799,2003,2200]
    rx21 = [210,469,633,861,1027,1131,1308,1423,1545,1602]
    rx31 = [198,356,412,533,569,601,633,690,702,711,706]
    r11 = []
    r21 = []
    r31 = []
    for i in range(10):
        r11.append(rx11[i]/(300*(i+1)))
        r21.append(rx21[i] / (300 * (i + 1)))
        r31.append(rx31[i] / (300 * (i + 1)))
    p4 = plt.plot(x, r11, marker='+')
    plt.plot(x, r21, marker='d')
    plt.plot(x, r31, marker='s')
    plt.legend(('GDWP', 'OLPM', 'greedy'), loc='upper left')
    plt.xlabel('SFC 数（个）', fontsize=15)
    plt.ylabel('接受率', fontsize=15)
    plt.show()
    plt.ylim(0,1)