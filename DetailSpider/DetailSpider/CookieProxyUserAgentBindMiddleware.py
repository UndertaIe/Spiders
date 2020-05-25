#!/usr/bin/python 
# -*- coding: utf-8 -*-

from utils.CookieHandler import getCookie
from utils.SleepUtil import sleepError

class CookieProxyUserAgentBindMiddleware(object):


    def process_request(self, request, spider):
        """从redis获取生成的cookie包括生成参数依次有Cookie，proxy，ua"""
        cookieAndProxy = getCookie()
        cookieKey = "__zp_stoken__"
        if cookieAndProxy is not None:
            # 设置cookie
            cookie = {cookieKey:cookieAndProxy[cookieKey]}
            request.cookies = cookie
            # 设置与cookie绑定生成的proxy
            proxy = cookieAndProxy['proxy']
            request.meta['proxy'] = 'http://' + proxy
            #设置与cookie绑定生成的User-Agent
            ua = cookieAndProxy['ua']
            request.headers.setdefault('User-Agent', ua)
        else:
            print("###[WARNING] Spider request didn't carry Cookie,Proxy,UserAgent,request may return error page ###")
            sleepError()

