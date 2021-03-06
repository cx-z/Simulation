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

Price_Graph = {
    0:{1:12,2:18,7:5},
    1:{0:12,2:20,3:20},
    2:{0:18,1:20,5:7},
    3:{1:20,4:11,10:6},
    4:{3:11,5:13,6:14},
    5:{2:7,4:13,9:13,12:10},
    6:{4:14,7:19},
    7:{0:5,6:19,8:17},
    8:{7:17,9:18,11:15,13:15},
    9:{5:13,8:18},
    10:{3:6,11:16,13:10},
    11:{8:15,10:16,12:19},
    12:{5:10,11:19,13:20},
    13:{8:15,10:10,12:20}
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
    (0,1):1000,(0,2):900,(0,7):500,
    (1,0):1000,(1,2):1000,(1,3):1000,
    (2,0):900,(2,1):1000,(2,5):700,
    (3,1):1000,(3,4):550,(3,10):600,
    (4,3):550,(4,5):650,(4,6):700,
    (5,2):700,(5,4):650,(5,9):650,(5,12):500,
    (6,4):850,(6,7):950,
    (7,0):500,(7,6):950,(7,8):850,
    (8,7):850,(8,9):900,(8,11):750,(8,13):750,
    (9,5):650,(9,8):900,
    (10,3):600,(10,11):800,(10,13):500,
    (11,8):750,(11,10):800,(11,12):950,
    (12,5):500,(12,11):950,(12,13):1000,
    (13,8):750,(13,10):500,(13,12):1000
}

DataCenters_Price = {
    0:12,1:11,2:10,3:13,
    4:11,5:14,6:13,7:12,
    8:10,9:11,10:15,11:14,
    12:15,13:10
}

DataCenters_CPU = {
    0:2000, 1:1600, 2:2100, 3:2200,
    4:1500, 5:2000, 6:1800, 7:1600,
    8:1400, 9:2400, 10:1900, 11:2600,
    12:2600, 13:1900
}