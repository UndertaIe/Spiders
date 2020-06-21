#!/usr/bin/python 
# -*- coding: utf-8 -*-

from utils.RedisHandler import RedisHandler
from utils.cityUitl import getHotCity,getAllCity
from utils.DriverHandler import getDriver
from utils.SleepUtil import sleepClear,sleepInput,sleepClick,sleepGet
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import sys


def startTask(Counter,searchKey,isHotCity):
    if isHotCity == "True":
        search(Counter,searchKey,searchMethod=hotCitySearch)
    elif isHotCity == "False":
        search(Counter,searchKey, searchMethod=allCitySearch)
    else:
        search(Counter, searchKey, searchMethod=hotCitySearch)

#searchMethod可增加搜索方法 在search方法中循环搜索 直到search key中无内容
def search(Counter,searchKey,searchMethod):
    r = RedisHandler(search=searchKey)
    driver = getDriver('chrome')
    while True:
        oneSearch = r.getSearch()
        if oneSearch is None:
            break
        searchMethod(driver=driver,oneSearch=oneSearch)
        Counter.value += 1

    driver.quit()
    r.close()

#热门城市搜索
def hotCitySearch(driver,oneSearch):
    mes = "-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-\n"
    mes += "###[INFO] HotCity Search {} is Starting. ###\n".format(oneSearch)
    mes += "-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-\n"
    sys.stdout.write(mes + '\n')
    sys.stdout.flush()
    Count = 0
    r1 = RedisHandler()
    hotcitys = getHotCity()
    #从官网搜索栏过渡 防止识别爬虫
    driver.get("https://www.zhipin.com/")
    sleepGet()
    driver.find_element_by_xpath('//div[@class="search-form-con"]/p/input').send_keys(oneSearch)
    sleepInput()
    # 获取按钮对象并点击
    button1 = driver.find_element_by_xpath('//button[@class="btn btn-search"]')
    driver.execute_script("arguments[0].click();",button1)
    sleepClick()
    for city in hotcitys:
        JobAndCity = oneSearch + city
        # 清理搜索框
        input_box = driver.find_element_by_xpath('//p[@class="ipt-wrap"]/input[@class="ipt-search"]')
        if input_box is not None:
            ActionChains(driver).move_to_element(input_box).perform()
            input_box.clear()
            #sleepClear()
            # 输入查询内容到搜索框
            input_box.send_keys(JobAndCity)
            #sleepInput()
            #模拟用户移动点击按钮元素查询数据
            button2 = driver.find_element_by_xpath('//button[@class="btn btn-search"]')
            ActionChains(driver).move_to_element(button2).click(button2).perform()
            sleepGet()
            # SelectURL
            selectUrl = driver.current_url
            # 插入城市查询URL
            flag = r1.insertSelectURL(oneSearch, selectUrl)
            if flag > 0:
                mes = ('###[SUCCESS] Select URL <{}> : {} >>> Redis <{}> select_urls ###'.format(city, selectUrl, oneSearch))
                Count += 1
                sys.stdout.write(mes + '\n')
                sys.stdout.flush()
            else:
                mes = ('###[WARNING] Select URL <{}> : {} -|- Redis <{}> select_urls ###'.format(city, selectUrl, oneSearch))
                sys.stdout.write(mes + '\n')
                sys.stdout.flush()

    search_len = r1.getSearchsLen()
    mes = ('\n###[INFO] HotCity Search <{}> end. Search Select Item count: <{}>.Redis Search remain <{}>###\n'.format(oneSearch, Count, search_len))
    sys.stdout.write(mes + '\n')
    sys.stdout.flush()
    r1.close()

#所有城市搜索
def allCitySearch(driver,oneSearch):
    mes = "-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-\n"
    mes += "###[INFO] AllCity Search <{}> is Starting. ###\n".format(oneSearch)
    mes += "-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-\n"
    sys.stdout.write(mes + '\n')
    sys.stdout.flush()

    Count = 0
    r2 = RedisHandler()
    provs = getAllCity()

    # 从官网搜索栏过渡 防止识别爬虫
    driver.get("https://www.zhipin.com/")
    sleepGet()
    driver.find_element_by_xpath('//div[@class="search-form-con"]/p/input').send_keys(oneSearch)
    # sleepInput()
    # 获取按钮对象并点击
    button1 = driver.find_element_by_xpath('//button[@class="btn btn-search"]')
    driver.execute_script("arguments[0].click();", button1)
    # driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/form/div/button').click()
    sleepClick()
    for prov in provs.keys():
        for city in provs[prov]:
            JobAndCity = oneSearch + city
            # 清理搜索框
            input_box = driver.find_element_by_xpath('//p[@class="ipt-wrap"]/input[@class="ipt-search"]')
            if input_box is not None:
                #模拟用户选择搜索框事件
                ActionChains(driver).move_to_element(input_box).perform()
                input_box.clear()
                # sleepClear()
                # 向搜索框输入查询内容
                input_box.send_keys(JobAndCity)
                # sleepInput()
                # 点击查询数据

                button2 = driver.find_element_by_xpath('//button[@class="btn btn-search"]')
                ActionChains(driver).move_to_element(button2).click(button2).perform()
                sleepGet()
                # SelectURL

                selectUrl = driver.current_url
                # 插入城市查询URL
                flag = r2.insertSelectURL(oneSearch, selectUrl)
                if flag > 0:
                    mes = ('###[SUCCESS] Select URL <{}> : {} >>> Redis <{}> select_urls ###'.format(city, selectUrl,oneSearch))
                    Count += 1
                    sys.stdout.write(mes + '\n')
                    sys.stdout.flush()
                else:
                    mes = ('###[WARNING] Select URL <{}> : {} -|- Redis <{}> select_urls ###'.format(city, selectUrl,oneSearch))
                    sys.stdout.write(mes + '\n')
                    sys.stdout.flush()


    search_len = r2.getSearchsLen()
    mes = ('\n###[INFO] AllCity Search <{}> end. Search Select Item count: <{}>.Redis Search remain <{}>###\n'.format(
        oneSearch, Count, search_len))
    sys.stdout.write(mes + '\n')
    sys.stdout.flush()
    r2.close()
