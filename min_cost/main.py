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
                cost1.append(cost/10)
                nnum1.append(nnum)
                enum1.append(enum)
                t1.append(end-start)
            elif i == 1:
                cost2.append(cost/10)
                nnum2.append(nnum)
                enum2.append(enum)
                t2.append(end - start)
            else:
                cost3.append(cost/10)
                nnum3.append(nnum)
                enum3.append(enum)
                t3.append(end - start)

    print(cost1)
    print(cost2)
    print(cost3)
    print(nnum1)
    print(nnum2)
    print(nnum3)
    print(nnum1)
    print(nnum2)
    print(nnum3)
    print(t1)
    print(t2)
    print(t3)

    p1 = plt.plot(x, cost1, x, cost2, x, cost3)
    plt.legend(('RDO','T-SAT','OLPM'),loc='upper right')
    plt.xlabel('SFC amount')
    plt.ylabel('deployment cost')
    plt.show()
    p2 = plt.plot(x, nnum1, x, nnum2, x, nnum3)
    plt.legend(('RDO', 'T-SAT', 'OLPM'), loc='upper right')
    plt.xlabel('SFC amount')
    plt.ylabel('purchase nodes num')
    plt.ylim(0,15)
    plt.show()
    p3 = plt.plot(x, enum1, x, enum2, x, enum3)
    plt.legend(('RDO', 'T-SAT', 'OLPM'), loc='upper right')
    plt.xlabel('SFC amount')
    plt.ylabel('purchase edges num')
    plt.ylim(0,24)
    plt.show()
