# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector
from time import sleep
from ..utils.RedisHandler import RedisHandler
import sys
import re
import random
import json
from ..settings import RESARCH_NAME
from selenium import webdriver
'''
Master:通过城市json文件解析出城市字典，循环此字典在搜索框中搜索指定工作类型和工作地点，得到对应工作地点的页面，存储到redis，之后交给slave来爬取。
'''
class BossSpider(RedisSpider):
    name = "master"
    #不同key对应不同的搜索内容
    redis_key = "Boss:{}:start_url".format(RESARCH_NAME)

    #Boss:start_url = https://www.zhipin.com/wapi/zpCommon/data/city.json  json城市文件


    def __init__(self):
        super(BossSpider, self).__init__()
        # 获取redis操作对象
        self.rehandler = RedisHandler()

        # {省份：城市}字典
        self.provs = {}
        # selenium启动选项
        options = webdriver.FirefoxOptions()
        # 设置为开发者模式
        options.add_argument("--headless")  # 设置火狐为headless无界面模式
        options.add_argument("--disable-gpu")
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Firefox(options=options, executable_path="C:\\CJP\\Python\\Scripts\\geckodriver.exe")
        self.driver.maximize_window()   # 浏览器最大化
        # self.driver.minimize_window() # 浏览器最小化
        # 获取Boos主页
        self.driver.get("https://www.zhipin.com/")
        sleep(2)

    # 生成城市搜索结果URL
    def parse(self, response):
        self.location(response) #生成{省份：城市}字典

        # ===从官网界面过度===
        # 获取Boos搜索框对象并输入python
        self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[1]/form/div[2]/p/input').send_keys(RESARCH_NAME)
        sleep(0.5)
        #获取按钮对象并点击
        self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[1]/form/button').click()
        sleep(2)

        # ====获取各个地区的查询结果页面存储到Redis。slave可使用这一selectURL来获取数据===
        for prov in self.provs.keys():
            for city in self.provs[prov]:
                search = RESARCH_NAME + city
                # 清理搜索框
                self.driver.find_element_by_xpath('//p[@class="ipt-wrap"]/input[@name="query"]').clear()
                # 向搜索框输入查询内容
                self.driver.find_element_by_xpath('//p[@class="ipt-wrap"]/input[@name="query"]').send_keys(search)
                sleep(0.5)
                # 点击查询数据
                self.driver.find_element_by_xpath('//button[@class="btn btn-search"]').click()
                sleep(2)

                # SelectURL
                selectUrl = self.driver.current_url
                # 插入城市查询URL
                self.rehandler.insertSelectURL(selectUrl)

        self.driver.quit()


    # 获取城市字典
    def location(self,response):
        json_text = json.loads(response.text)['zpData']['cityList']
        # 将json文件转化为字典dic 结构为 dic = {province0:[city0,city1,city2],province1:[city0,city1,city2]...}
        for i in range(len(json_text)):
            # 获取省份名
            province = json_text[i]['name']
            # 获取所在省份 城市列表
            provinces = json_text[i]['subLevelModelList']
            self.provs.setdefault(province, [])
            citys = []
            # 分类直辖市和地级市，并归类到字典的值
            if provinces.__len__() > 1:
                for ii in range(len(provinces)):
                    citys.append(provinces[ii]['name'])
            else:
                citys.append(province)
            self.provs[province] = citys
