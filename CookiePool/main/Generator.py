# coding:utf-8

from gevent import monkey
monkey.patch_all()
import sys
import time
from gevent.pool import Pool
from config import POOLSIZE
from main.DbManager import dbHandler
from config import COOKIE_MIN,COOKIE_URLS,UPDATE_TIME,SplashUrl
from time import sleep
import random
from utils.ProxyHandler import getProxy,getChargeProxy
from utils.UserAgentHandler import getUserAgent
from utils.SleepUtil import sleepCookie
from config import SplashAuthUser,SplashAuthPwd
import requests
import json

def startCookiePool(buffer, cookieCounter, gen_cookie_num, useProxy):
    cookiegen = CookieGenerator(buffer,cookieCounter,gen_cookie_num,useProxy)
    cookiegen.run()

class CookieGenerator:

    def __init__(self, buf, cookieCounter, gen_cookie_num, useProxy):
        self.cookie_pool =Pool(POOLSIZE)
        self.handler = dbHandler
        self.cookieCounter = cookieCounter  #实时个数 易变
        self.gen_cookie_num = gen_cookie_num #要生成的cookie个数
        self.useProxy = useProxy
        self.buffer = buf
        self.splashUrl = ""
        self.luaScript = ""
        self.init_splash()

    def init_splash(self):
        self.splashUrl = SplashUrl
        if self.useProxy:
            with open("main/getCookie.lua") as f: #使用代理脚本
                self.luaScript = f.read()
        else:
            with open("main/getCookieNoProxy.lua") as f: # 不使用代理脚本
                self.luaScript = f.read()

                # splash.images_enabled = false

    def run(self):
        while True:
            mes =" | CookiePool | ------>>>>>>>>Begining"
            sys.stdout.write(mes+'\r\n')
            sys.stdout.flush()
            self.cookieCounter.value = self.handler.count()
            mes = ' | CookiePool | ------>>>>>>>>db exists cookie:{}'.format(self.cookieCounter.value)
            if self.cookieCounter.value < self.gen_cookie_num.value:
                mes += '\r\n | CookiePool | ------>>>>>>>>Now cookie num < MINNUM,start gernerating...'
                sys.stdout.write(mes + "\r\n")
                sys.stdout.flush()
                self.cookie_pool.map(self.getCookie, COOKIE_URLS)
            else:
                mes += '\r\n | CookiePool | ------>>>>>>>>Now cookie num meet the requirement,wait UPDATE_TIME...'
                mes += '\r\n | CookiePool | ------>>>>>>>>Sleep now......'
                sys.stdout.write(mes + "\r\n")
                sys.stdout.flush()
                time.sleep(UPDATE_TIME)

    def getCookie(self, COOKIE_URL):
        ua = getUserAgent()

        lua_source = self.luaScript.replace("*url*",COOKIE_URL)
        if ua is not None:
            lua_source.replace("*UA*", ua)

        if self.useProxy:
            aproxy = getProxy()  # 设置实时有效代理IP 否则并发环境下 爬虫速度过高容易被检测出来
            # aproxy = getChargeProxy()  # 设置收费代理

            if aproxy is not None:
                proxy = aproxy.get('proxy')
                proxy_host,proxy_port = proxy.split(':')
                lua_source = lua_source.replace("*proxy_host*",proxy_host)   #在lua脚本中更换IP代理
                lua_source = lua_source.replace("*proxy_port*", proxy_port)

        data = {'timeout': 20, 'lua_source': lua_source}

        for i in range(4):
            try:
                # ['Content-Type'] = 'application/json'
                # r = requests.post(url=self.splashUrl, data=json.dumps(data), headers={'Content-Type': 'application/json'}, auth=(SplashAuthUser,SplashAuthPwd))
                r = requests.post(url=self.splashUrl, data=json.dumps(data), headers={'Content-Type': 'application/json'},timeout=20)
                if r.status_code == 200:
                    raw_cookies = r.json()
                    if raw_cookies is not None:
                        cookie = self.splash2cookie(raw_cookies)
                        # 本机测试不设置代理
                        if self.useProxy:
                            cookie.setdefault('proxy', proxy)  # 设置有效代理
                        cookie.setdefault('ua', ua)
                        self.buffer.put(cookie)
            except:
                print("###[WARNING] Remote Splash Service didn't work well ###")

            sleepCookie() # 防止频率过高封IP,使用代理可减去休眠时间

    @staticmethod
    def splash2cookie(raw_cookies):
        key = "__zp_stoken__"
        if isinstance(raw_cookies,list):
            return { key:cookie.get('value') for cookie in raw_cookies if key == cookie.get('name') }