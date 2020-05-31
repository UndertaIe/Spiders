#!/usr/bin/python 
# -*- coding: utf-8 -*-

from .utils.CookieHandler import getCookie
from .utils.SleepUtil import sleepError

class CookieProxyUserAgentBindMiddleware(object):


    def process_request(self, request, spider):
        """从redis获取生成的cookie包括生成参数依次有Cookie，proxy，ua"""
        search = spider.search
        cookieAndProxy = getCookie()
        cookieKey = "__zp_stoken__"

        print("-*-got Cookie:-*-")  #测试用
        print(cookieAndProxy)   #测试用
        print("-*-got Cookie:-*-")   #测试用

        if cookieAndProxy is not None:
            # 设置cookie
            cookieDic = {cookieKey:cookieAndProxy.get(cookieKey)}
            request.cookies = cookieDic


            # 设置与cookie绑定生成的proxy
            # proxy = cookieAndProxy.get('proxy')  # 本地测试 不设置代理
            # request.meta['proxy'] = 'http://' + proxy

            #设置与cookie绑定生成的User-Agent
            ua = cookieAndProxy.get('ua')
            request.headers.setdefault('User-Agent', ua)
        else:
            print("###[WARNING] CookieProxyUserAgentBindMiddleware <{}> Spider request didn't carry Cookie,Proxy,UserAgent ###".format(search))
            sleepError()

