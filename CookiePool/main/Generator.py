# coding:utf-8

from gevent import monkey
monkey.patch_all()
import sys
import time
from gevent.pool import Pool
from config import POOLSIZE
from main.DbManager import dbHandler
from config import COOKIE_MIN,COOKIE_URLS,UPDATE_TIME,User_Agent,SplashUrl
from time import sleep
import random
from utils.ProxyHandler import getProxy
import requests
import json

def startCookiePool(buffer,cookieCounter,gen_cookie_num):
    luaScript = ""
    with open("getCokLua.lua") as f:
        luaScript = f.read()
    cookiegen = CookieGenerator(buffer,cookieCounter,gen_cookie_num)
    cookiegen.run()

class CookieGenerator:

    def __init__(self,buf,cookieCounter,gen_cookie_num=COOKIE_MIN):
        self.cookie_pool =Pool(POOLSIZE)
        self.handler = dbHandler
        self.cookieCounter = cookieCounter  #实时个数 易变
        self.gen_cookie_num = gen_cookie_num #要生成的cookie个数
        self.buffer = buf
        self.userAgents = None
        self.splashUrl = ""
        self.luaScript = ""
    def init_splash(self):
        self.userAgents = User_Agent
        self.splashUrl = SplashUrl
        with open("getCokLua.lua") as f:
            self.luaScript = f.read()

    def run(self):
        while True:
            mes =" | CookiePool | ------>>>>>>>>begining"
            sys.stdout.write(mes+'\r\n')
            sys.stdout.flush()
            self.cookieCounter.value = self.handler.count()
            mes = ' | CookiePool | ------>>>>>>>>db exists cookie:%d' % self.cookieCounter.value
            if self.cookieCounter.value < self.gen_cookie_num:
                mes += '\r\n | CookiePool | ------>>>>>>>>now cookie num < MINNUM,start gernerating...'
                sys.stdout.write(mes + "\r\n")
                sys.stdout.flush()
                self.cookie_pool.map(self.getCookie,COOKIE_URLS)
            else:
                mes += '\r\n | CookiePool | ------>>>>>>>>now cookie num meet the requirement,wait UPDATE_TIME...'
                mes += '\r\n | CookiePool | ------>>>>>>>>Sleep now......'
                sys.stdout.write(mes + "\r\n")
                sys.stdout.flush()
                time.sleep(UPDATE_TIME)

    def getCookie(self,COOKIE_URL):
        lua_source = self.luaScript.replace("*url*",COOKIE_URL)
        ua = random.choice(self.userAgents)
        aproxy = getProxy()
        params = {}
        if aproxy is not None:
            params.setdefault('proxies',"http://{}".format(aproxy['proxy']))
        params.setdefault("user-agent",ua)
        params.setdefault('lua_script',lua_source)
        headers = {"content-type": "application/json"}
        for i in range(5):
            r = requests.post(url=self.splashUrl,data=json.dumps(params),headers=headers)
            raw_cookies = r.json()
            if raw_cookies is not None:
                cookie = self.splash2cookie(raw_cookies)
                self.buffer.put(cookie)
            sleep(2)#防止频率过高封IP

    @staticmethod
    def splash2cookie(raw_cookies):
        key = "__zp_stoken__"
        return { key:cookie['value'] for cookie in raw_cookies if key == cookie['name'] }