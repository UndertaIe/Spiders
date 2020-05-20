#!/usr/bin/python 
# -*- coding: utf-8 -*-

# coding:utf-8

from gevent import monkey
monkey.patch_all()
import sys
import time
from gevent.pool import Pool
from config import POOLSIZE,HEADLESS_NUM
from main.DbManager import dbHandler
from config import COOKIE_MIN,COOKIE_URLS,UPDATE_TIME
from selenium import webdriver
from time import sleep


def startCookiePool(buffer,cookieCounter,gen_count):
    cookieGen = CookieGenerator(buffer,cookieCounter,gen_count)
    cookieGen.run()

class CookieGenerator:
    count = 0
    def __init__(self,buf,cookieCounter,gen_cookie_num=COOKIE_MIN):
        self.cookie_pool =Pool(POOLSIZE)  #设置并发协程数
        self.handler = dbHandler #redis对象
        self.cookieCounter = cookieCounter  #实时个数 易变
        self.genCount = gen_cookie_num #要生成的cookie个数
        self.buffer = buf
        self.drivers = []
        CookieGenerator.count += 1
        self.id = CookieGenerator.count
    def init_driver(self):
        self.shutdown_driver()
        options = webdriver.FirefoxOptions()
        # 设置为开发者模式
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument("--headless")  # 设置火狐为headless无界面模式
        options.add_argument("--disable-gpu")
        options.add_argument('blink-settings=imagesEnabled=false') #不加载图片
        options.add_argument('--no-sandbox') #非安全模式
        #options.add_argument("--proxy-server=http://202.20.16.82:10152") #添加静态代理
        for i in range(HEADLESS_NUM):
            driver = webdriver.Firefox(options=options, executable_path="C:\\CJP\\Python\\Scripts\\geckodriver.exe")
            self.drivers.append(driver)

    def shutdown_driver(self):
        for driver in self.drivers:
            driver.close()
            driver.quit()
        self.drivers = []
    def run(self):
        mes = " | CookiePool:{} | ------>>>>>>>> begining\n".format(self.id)
        sys.stdout.write(mes)
        sys.stdout.flush()
        while True:
            self.cookieCounter.value = self.handler.count()
            mes = ' | CookiePool:{} | ------>>>>>>>> db exists cookie:{}\n'.format(self.id,self.cookieCounter.value)
            if self.cookieCounter.value < self.genCount.value:
                mes += ' | CookiePool:{} | ------>>>>>>>> now cookie num < MINNUM,start gernerating...\n'.format(self.id)
                self.init_driver()
            sys.stdout.write(mes)
            sys.stdout.flush()

            while self.cookieCounter.value < self.genCount.value: #数据库cookie个数小于指定的数目则持续生成cookie
                self.cookie_pool.map(self.getCookie,self.drivers)

            mes += ' | CookiePool:{} | ------>>>>>>>> now cookie num meet the requirement,wait UPDATE_TIME...\n'.format(self.id)
            mes += ' | CookiePool:{} | ------>>>>>>>> Sleep now......\n'.format(self.id)
            sys.stdout.write(mes)
            sys.stdout.flush()
            self.shutdown_driver()
            time.sleep(UPDATE_TIME)

    def getCookie(self,driver):
        driver.delete_all_cookies()
        for url in COOKIE_URLS:
            driver.delete_all_cookies()
            driver.get(url)
            sleep(4)
            raw_cookie = driver.get_cookies()
            driver.delete_all_cookies()
            if raw_cookie is not None:
                cookie = self.driver2cookie(raw_cookie)
                self.buffer.put(cookie)


    # @staticmethod
    # def driver2cookie(cookie_from_driver):
    #     cookie = {}
    #     for coo in cookie_from_driver:
    #         cookie.setdefault(coo['name'], coo['value'])
    #     return cookie

    @staticmethod
    def driver2cookie(cookie_from_driver):
        key = "__zp_stoken__"
        for coo in cookie_from_driver:
            if coo['name'] == key:
                return {key:coo['value']}
        return None