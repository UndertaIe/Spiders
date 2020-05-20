#!/usr/bin/python 
# -*- coding: utf-8 -*-
import os
from utils.RedisHandler import RedisHandler
import re

#可在此方法中修改参数，通过不同参数不同方式导入到Redis search key中
def initSearch(jobList,jobPath,searchKey):
    if isinstance(jobList,tuple):
        searchs = [job for job in jobList]
    if isinstance(jobList,str):
        result = re.split("\,|\，|\.|\;|\:|\!|\@|\#|\$|\%|\^|\&|\*|\-|\+|\_",jobList) # .可以去掉防止.net类的岗位出现错误
        searchs = result if result[0] != "" else []
    if os.path.isfile(jobPath):
        with open(jobPath, encoding="utf-8-sig") as f:  #读出search
            searchs.extend([line.strip() for line in f.readlines() if line.strip()!=""])
        with open(jobPath,'w') as f:  #读出后清空文件
            f.write("")
    insertRedisSearch(searchs,searchKey)

def insertRedisSearch(searchs,searchKey):
    r = RedisHandler(search=searchKey)
    for search in searchs:
        flag = r.insertSearch(search)
        if flag != 0:
            print("###[SUCCESS] InitSearch {} >>> Redis Search key ###".format(search))
        else:
            print("###[ERROR] InitSearch {} -|- Redis Search key ###".format(search))
    search_len = r.getSearchsLen()
    print("###[INFO] Redis key <Search> remains: <{}> ###".format(search_len))

    r.close()
