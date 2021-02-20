#-*-coding:utf-8-*-
import random
import os

#生成请求的流量序列
def bandSeq(bandwidth:int)->list:
    seq = [0 for _ in range(10)]
    for i in range(10):
        seq[i] = random.randint(0,bandwidth)
    return seq

#生成vnf序列
def make_sfc()->list:
    num = random.randint(2,10)
    t_sfc = set()
    for i in range(num):
        vnf = "vnf"+str(random.randint(0,9))
        if vnf not in t_sfc:
            t_sfc.add(vnf)
        else:
            i -= 1
    sfc = list()
    for v in t_sfc:
        sfc.append(v)
    return sfc

# 生成请求信息并写在requests.txt文件中
# 参数为打算生成的请求数
def req_info(cnt:int)->None:
    os.system("rm requests.txt")
    for i in range(cnt):
        id = i # id
        src = random.randint(0,13) # src
        dst = random.randint(0,13) # dst
        while dst == src:
            dst = random.randint(0,13)
        band = random.randint(1,10) # bandwidth
        bid = random.randint(1,5)*band*100 # 用户出价
        maxDelay = random.randint(10,30)*1000
        sfc = make_sfc()
        line1 = "{} {} {} {} {} {} "\
            .format(str(id),str(src),str(dst),str(band),str(bid),str(maxDelay))
        for v in sfc:
            line1 += v + " "
        seq = bandSeq(band)
        line2 = ""
        for i in seq:
            line2 += str(i) + " "
        with open('requests.txt','a+') as f:    #设置文件对象
            f.write(line1+'\n')
            f.write(line2+'\n')  
        
req_info(100)