#!/usr/bin/python
# -*- coding: utf-8 -*-

import fire
import sys,os
from multiprocessing import Process,Value
from Task.TaskBuilder import startTask
from Task.SearchInit import initSearch
from config import SEARCH,HOTCITY,HEADERS
from time import perf_counter

#可添加多进程 但有速度太快被反爬虫检测出来的风险 解决方案：可在selenium浏览器中中添加代理IP，经过一段时间更换IP
def task(List="",Path="",hotCity=HOTCITY,searchKey=SEARCH):
    '''

    :param List: 初始化Boss:search的元组参数
    :param Path: 初始化Boss:search的文件类型参数
    :param hotCity: 搜索是否是热门城市
    :param searchKey: 搜索项的redis key
    :return:
    '''
    try:
        print(HEADERS)
        start = perf_counter()
        JobCounter = Value('i',0)
        initSearch(List,Path,searchKey)
        pro1 = Process(target=startTask,args=(JobCounter,searchKey,hotCity))
        #pro2 = Process(target=startTask,args=(JobCounter,searchKey,hotCity))
        print("###[INFO] Task Builder Process is running... ###")
        pro1.start()
        #pro2.start()
        pro1.join()
        #pro2.join()
        # if ~(pro1.is_alive() and pro2.is_alive()):
        if ~pro1.is_alive():
            pro1.terminate()
            end = perf_counter()
            print("###[INFO] Task Builder Process terminated. Search Count: <{}>. Search elapsed time: <{}> ###".format(
                JobCounter.value, end - start))
        #    pro2.terminate()
    except KeyboardInterrupt:
        pass
    except:
        print("###[WARNING]Unknown ERROR occurred,Exiting...... ###")
        os.system("taskkill /im chrome.exe /F")
        os.system("taskkill /im chromedriver.exe /F")
        sys.exit(0)
if __name__ == '__main__':
    fire.Fire()