from time import sleep
from typing import Optional
from fastapi import APIRouter
import idna
import os
import json

task31 = APIRouter(prefix="/task1")
data_path ="data/task1/"

class Node():
    def __init__(self,name,id,label,risk) -> None:
        self.name = name
        self.id = id
        self.label = label
        self.risk = risk

class Edge():
    def __init__(self,beg_time,end_time,label,ids) -> None:
        self.beg_time = beg_time
        self.end_time = end_time
        self.label = label
        self.ids = ids

        
class Pattern():
    def __init__(self,edges,pid,id) -> None:
        self.id = id
        self.risk = 1
        #self.ids =[]
        self.edges = edges
        self.pid = pid

def gen_cyc(len):
    id = 0
    #beg_time = 0
    edges =[]
    for j in range(len):
        nodes = []
        for i in range(3):
            nodes.append(Node("company"+str(id),id,1,1))
            id = id+1
        edges.append(Edge(None,None,"持股关系",nodes))
        id = id - 1
    edges[-1].ids.append(Node("company"+str(0),0,1,1))
    return Pattern(edges)


def gen_cyc1(str_line):
    
    edges  = []
    id = 0
    
    with open(file_name,'r') as f:
        for line in f:
            nodes = []
            line = line.replace("\n","")
            coms = line.split(" ")
            for com in coms:
                nodes.append(Node(com,id,1,1))
                id = id+1
            edges.append(Edge(None,None,"持股关系",nodes))
                
    return Pattern(edges)

def gen_from_str(str_line):
    list_str = str_line.split("#")
    pid = list_str[0].split(";")[0]
    tid = list_str[0].split(";")[1]
    str_line = list_str[1]
    edges = []
    id = 0
    lines = str_line.split(";")
    for line in lines:
        nodes = []
        coms = line.split(" ")
        for com in coms:
            l = com.split("@")
            com = l[0]
            risk = l[1]
            nodes.append(Node(com,com,1,risk))
        edges.append(Edge(None,None,"持股关系",nodes))
    return Pattern(edges,pid,tid)

def test():

    r =[]
    file_dir = data_path+"task1.data"
    with open(file_dir,'r') as f:
        for line in f:
            r.append(gen_from_str(line))
    #str1 = "1;3#常林股份 苏美达集团;苏美达集团 中国进口汽车贸易有限公司 国机资本;国机资本 国机财务 常林股份"
    #str2 =  "1;2#东莞市东阳光实业发展有限公司 广东东阳光科技控股股份有限公司;广东东阳光科技控股股份有限公司 宜昌东阳光药业 深圳市东阳光实业发展有限公司;宜昌东阳光药业 南北兄弟药业投资有限公司 东莞市东阳光实业发展有限公司"
    #str3 = "-1;1#company1 company2;company2 company4 company3;company3 company5 company1"
    #return [gen_from_str(str1),gen_from_str(str2),gen_from_str(str3)]
    return r
#print(test())    
@task31.get("/")
def hello():
    return "h;"

@task31.get("/file")
def readF(file_name):
    data = open(data_path+file_name,'r')
    return json.load(data)

@task31.get("/1")
def miner(support,data,time):
    #sleep(5)
    #mse = {"pattern_nums": 3, "patterns_list":test()}
    #return mse 
    file_name = data+"_"+time+"_"+support+"_all_5_motif.json"
    data = open(data_path+file_name,'r')
    return json.load(data)

@task31.get("/risk_ex")
def risk_ex():
    return readF("risk.json")


@task31.get("/mine_info")
def fun1():
    data = open(data_path+"1.data",'r')
    return json.load(data)

@task31.get("/risk_info")
def fun2():
    data = open(data_path+"2.data",'r')
    return json.load(data)



@task31.get("/task12")
def queryRisk():
    pass 



'''
    str1 = "常林股份 苏美达集团;苏美达集团 中国进口汽车贸易有限公司 国机资本;国机资本 国机财务 常林股份"
    str2 =  "雅克科技 南京华瑞一号;南京华瑞一号 江苏图治信息科技有限公司 江苏华瑞;江苏华瑞 香港中央结算有限公司 雅克科技"
    str3 = "company1 company2;company2 company4 company3;company3 company5 company1"
            "东莞市东阳光实业发展有限公司 广东东阳光科技控股股份有限公司;广东东阳光科技控股股份有限公司 宜昌东阳光药业 深圳市东阳光实业发展有限公司;宜昌东阳光药业 南北兄弟药业投资有限公司 东莞市东阳光实业发展有限公司"


风帆股份（600482）与武汉船机、中船投资的交叉持股案
公司 股东
    
风帆有限责任公司：中国船舶重工集团动力股份有限公司
中国船舶重工集团动力股份有限公司：中国船舶重工股份有限公司，中国信达资产管理股份有限公司，中国证券金融股份有限公司，中国华融资产管理股份有限公司
武汉船用机械有限责任公司:中国船舶重工集团动力股份有限公司
中国船舶重工股份有限公司:

东莞市东阳光实业发展有限公司 ： 广东东阳光科技控股股份有限公司
广东东阳光科技控股股份有限公司 ： 宜昌东阳光药业 ，深圳市东阳光实业发展有限公司
宜昌东阳光药业 ：宜昌东阳光健康药业有眼公司，南北兄弟药业投资有限公司， 东莞市东阳光实业发展有限公司
ps -efww|grep -w 'uvicorn'|grep -v grep|cut -c 9-15|xargs kill -9
'''