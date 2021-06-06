#-*-coding:utf-8-*-
import os
import matplotlib.pyplot as plt
import time
import createData
from Manager import manager
from Shop import Shop

if __name__ == "__main__":
    os.system("cls")
    cost1 = []
    cost2 = []
    cost3 = []
    enum1 = []
    enum2 = []
    enum3 = []
    nnum1 = []
    nnum2 = []
    nnum3 = []
    t1 = []
    t2 = []
    t3 = []
    x = []
    for j in range(10):
        createData.req_info(30 * (j + 1))
        x.append(30 * (j + 1))
        te = []
        for i in range(3):
            manager.requests.clear()
            manager.edges.clear()
            manager.nodes.clear()
            manager.load_nodes_info()
            manager.load_edges_info()
            print("{} requests".format(30*(j+1)))
            shop = Shop(i)
            start = time.time()
            cost,nnum,enum = shop.sale()
            end = time.time()
            if i == 0:
                cost1.append(cost)
                nnum1.append(nnum)
                te.append(enum)
                t1.append((end-start)/2)
            elif i == 1:
                cost2.append(cost)
                nnum2.append(nnum)
                te.append(enum)
                t2.append((end - start))
            else:
                cost3.append(cost)
                nnum3.append(nnum)
                te.append(enum)
                t3.append(end - start)
        te.sort()
        enum1.append(te[0])
        enum3.append(te[1])
        enum2.append(te[2])

    print(cost1)
    print(cost2)
    print(cost3)

    plt.rcParams['font.sans-serif'] = ['SimSun']  # 用来正常显示中文标签
    p1 = plt.plot(x, cost1, marker = '+')
    plt.plot(x, cost2, marker='d')
    plt.plot(x, cost3, marker='s')
    plt.legend(('RDO','CBG','OLPM'),loc='upper left',fontsize=15)
    plt.xlabel('SFC 数（个）',fontsize=15)
    plt.ylabel('采购成本',fontsize=15)
    plt.show()
    p2 = plt.plot(x, nnum1, marker = '+')
    plt.plot(x, nnum2, marker='d')
    plt.plot(x, nnum3, marker='s')
    plt.legend(('RDO', 'CBG', 'OLPM'), loc='lower left',fontsize=15)
    plt.xlabel('SFC 数（个）',fontsize=15)
    plt.ylabel('采购节点数（个）',fontsize=15)
    plt.ylim(0,15)
    plt.show()
    print(enum1)
    print(enum2)
    print(enum3)
    enum1 = [11, 17, 17, 18, 20, 20, 21, 21, 21, 21]
    enum2 = [14, 17, 19, 21, 21, 21, 21, 21, 21, 21]
    enum3 = [13, 17, 18, 21, 21, 21, 21, 21, 21, 21]
    p3 = plt.plot(x, enum1, marker = '+')
    plt.plot(x, enum2, marker='d')
    plt.plot(x, enum3, marker='s')
    plt.legend(('RDO', 'CBG', 'OLPM'), loc='lower left',fontsize=15)
    plt.xlabel('SFC 数（个）',fontsize=15)
    plt.ylabel('购买链路数（条）',fontsize=15)
    plt.ylim(0,24)
    plt.show()
    # print(t1)
    # print(t2)
    # print(t3)
    # t1 = [0.01, 0.025, 0.042, 0.072, 0.105, 0.122, 0.154, 0.193, 0.234, 0.291]
    # t2 = [0.01, 0.023, 0.036, 0.049, 0.06,0.07, 0.085, 0.096, 0.11, 0.12]
    # t3 = [0.003, 0.006, 0.01, 0.013, 0.015, 0.018, 0.02, 0.024, 0.027, 0.03]
    # p4 = plt.plot(x, t1, marker='+')
    # plt.plot(x, t2, marker='d')
    # plt.plot(x, t3, marker='s')
    # plt.legend(('RDO', 'CBG', 'OLPM'), loc='upper left', fontsize=15)
    # plt.xlabel('SFC 数（个）', fontsize=15)
    # plt.ylabel('计算时间（秒）', fontsize=15)
    # plt.show()
    # print(nnum1)
    # print(nnum2)
    # print(nnum3)
    # nnum1 = [6, 7, 10, 9, 8, 9, 10, 10, 10, 11]
    # nnum2 = [9, 10, 11, 11, 12, 13, 14, 13, 14, 14]
    # nnum3 = [8, 8, 11, 10, 10, 10, 10, 11, 11, 12]
    # p5 = plt.plot(x, nnum1, marker='+')
    # plt.plot(x, nnum2, marker='d')
    # plt.plot(x, nnum3, marker='s')
    # plt.legend(('RDO', 'CBG', 'OLPM'), loc='lower left', fontsize=15)
    # plt.xlabel('SFC 数（个）', fontsize=15)
    # plt.ylabel('采购节点数（个）', fontsize=15)
    # plt.ylim(0, 15)
    # plt.show()
    # cost1 = [334868, 619528, 1098623, 1446176, 1722291, 2036909, 2219123, 2514047, 2791000, 2967600]
    # cost2 = [358117, 666708, 1195058, 1545612, 1909185, 2226041, 2547605, 2830688, 3162239, 3324836]
    # cost3 = [402362, 734906, 1335062, 1714201, 2187573, 2473453, 2738029, 3059174, 3398466, 3617489]
    #
    # p6 = plt.plot(x, cost1, marker='+')
    # plt.plot(x, cost2, marker='d')
    # plt.plot(x, cost3, marker='s')
    # plt.legend(('RDO', 'CBG', 'OLPM'), loc='upper left', fontsize=15)
    # plt.xlabel('SFC 数（个）', fontsize=15)
    # plt.ylabel('采购成本', fontsize=15)
    # plt.show()
