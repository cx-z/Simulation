#-*-coding:utf-8-*-

DURATION = 30

GRAPH = {
    0:{1:1100,2:1000,7:2800},
    1:{0:1100,2:600,3:1000},
    2:{0:1000,1:600,5:2000},
    3:{1:1000,4:600,10:2400},
    4:{3:600,5:1100,6:800},
    5:{2:2000,4:1100,9:1200,12:2000},
    6:{4:800,7:700},
    7:{0:2800,6:700,8:700},
    8:{7:700,9:900,11:300,13:500},
    9:{5:1200,8:900},
    10:{3:2400,11:800,13:800},
    11:{8:300,10:800,12:500},
    12:{5:2000,11:500,13:300},
    13:{8:500,10:800,12:300}
}

# 单位算力的处理时延，后续写生成随机数的代码补全
VNF_DELAY = {
    "vnf0":1, "vnf1":8, "vnf2":5, "vnf3":1, "vnf4":9,
    "vnf5":4, "vnf6":3, "vnf7":2, "vnf8":7, "vnf9":6
}

Edge_UnitPrice = {
    (0,1):12,(0,2):18,(0,7):5,
    (1,0):12,(1,2):20,(1,3):20,
    (2,0):18,(2,1):20,(2,5):7,
    (3,1):20,(3,4):11,(3,10):6,
    (4,3):11,(4,5):13,(4,6):14,
    (5,2):7,(5,4):13,(5,9):13,(5,12):10,
    (6,4):14,(6,7):19,
    (7,0):5,(7,6):19,(7,8):17,
    (8,7):17,(8,9):18,(8,11):15,(8,13):15,
    (9,5):13,(9,8):18,
    (10,3):6,(10,11):16,(10,13):10,
    (11,8):15,(11,10):16,(11,12):19,
    (12,5):10,(12,11):19,(12,13):20,
    (13,8):15,(13,10):10,(13,12):20
}

Edge_Band = {
    (0,1):100,(0,2):180,(0,7):50,
    (1,0):100,(1,2):200,(1,3):200,
    (2,0):180,(2,1):200,(2,5):70,
    (3,1):200,(3,4):110,(3,10):60,
    (4,3):110,(4,5):130,(4,6):140,
    (5,2):70,(5,4):130,(5,9):130,(5,12):100,
    (6,4):140,(6,7):190,
    (7,0):50,(7,6):190,(7,8):170,
    (8,7):170,(8,9):180,(8,11):150,(8,13):150,
    (9,5):130,(9,8):180,
    (10,3):60,(10,11):160,(10,13):100,
    (11,8):150,(11,10):160,(11,12):190,
    (12,5):100,(12,11):190,(12,13):200,
    (13,8):150,(13,10):100,(13,12):200
}

DataCenters_Price = {
    0:120,1:110,2:100,3:130,
    4:110,5:140,6:130,7:120,
    8:100,9:110,10:150,11:140,
    12:150,13:100
}

DataCenters_CPU = {
    0:700, 1:400, 2:300, 3:800,
    4:700, 5:600, 6:200, 7:300,
    8:800, 9:200, 10:800, 11:800,
    12:500, 13:500
}