# coding:utf-8

import gevent
from gevent import monkey

import sys
import time
from gevent.pool import Pool
from multiprocessing import Queue, Process, Value
from config import POOLSIZE,HEADLESS_NUM
from db.DbManager import dbHandler
from config import COOKIE_MIN,COOKIE_URLS,UPDATE_TIME
from selenium import webdriver
import random

monkey.patch_all()
def startCookiePool(buffer,cookieCounter):
    cookiegen = CookieGenerator(buffer,cookieCounter)
    cookiegen.run()


class CookieGenerator:

    def __init__(self,buf,cookieCounter):
        self.cookie_pool =Pool(POOLSIZE)
        self.handler = dbHandler
        self.cookieCounter = cookieCounter
        self.buffer = buf
        self.drivers = []
    def init_driver(self):
        self.shutdown_driver()
        options = webdriver.FirefoxOptions()
        # 设置为开发者模式
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument("--headless")  # 设置火狐为headless无界面模式
        options.add_argument("--disable-gpu")
        for i in range(HEADLESS_NUM):
            driver = webdriver.Firefox(options=options, executable_path="C:\\CJP\\Python\\Scripts\\geckodriver.exe")
            self.drivers.append(driver)
    def shutdown_driver(self):
        for driver in self.drivers:
            driver.quit()
        self.drivers = []
    def run(self):
        while True:
            mes =" | CookiePool | ------>>>>>>>>begining"
            sys.stdout.write(mes+'\r\n')
            sys.stdout.flush()
            self.cookieCounter.value = self.handler.count()
            mes = ' | CookiePool | ------>>>>>>>>db exists cookie:%d' % self.cookieCounter.value
            if self.cookieCounter.value < COOKIE_MIN:
                mes += '\r\n | CookiePool | ------>>>>>>>>now cookie num < MINNUM,start gernerating...'
                sys.stdout.write(mes + "\r\n")
                sys.stdout.flush()
                self.init_driver()
                self.cookie_pool.map(self.getCookie,self.drivers)
            else:
                mes += '\r\n | CookiePool | ------>>>>>>>>now cookie num meet the requirement,wait UPDATE_TIME...'
                mes += '\r\n | CookiePool | ------>>>>>>>>Sleep now......'
                self.shutdown_driver()
                sys.stdout.write(mes + "\r\n")
                sys.stdout.flush()
                time.sleep(UPDATE_TIME)

    def getCookie(self,driver):
        for i in range(5):
            for url in COOKIE_URLS:
                driver.get(url)
                #time.sleep(1)
                raw_cookie = driver.get_cookies()
                driver.delete_all_cookies()  #清除浏览器Cookie重新获得Cookie
                if raw_cookie is not None:
                    self.buffer.put(raw_cookie)