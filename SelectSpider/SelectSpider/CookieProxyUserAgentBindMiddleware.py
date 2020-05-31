#!/usr/bin/python 
# -*- coding: utf-8 -*-

from .utils.CookieHandler import getCookie
from .utils.SleepUtil import sleepWarn

class CookieProxyUserAgentBindMiddleware(object):


    def process_request(self, request, spider):
        """从redis获取生成的cookie包括生成参数依次有Cookie，proxy，ua"""

        search = spider.search
        cookieAndProxy = getCookie()

        print("---got Cookie:---")
        print(cookieAndProxy)
        print("---got Cookie:---")

        cookieKey = "__zp_stoken__"
        if cookieAndProxy is not None:
            # 设置cookie
            cookieDic = {cookieKey:cookieAndProxy.get(cookieKey)}
            request.cookies = cookieDic

            # 本地测试 不设置代理
            # 设置与cookie绑定生成的proxy
            # proxy = cookieAndProxy.get('proxy')
            # request.meta['proxy'] = 'http://' + proxy

            #设置与cookie绑定生成的User-Agent
            ua = cookieAndProxy.get('ua')
            request.headers.setdefault('User-Agent', ua)
        else:
            print("###[WARNING] CookieProxyUserAgentBindMiddleware <{}> Spider request didn't set Cookie,Proxy,UserAgent ###".format(search))
            sleepWarn()

