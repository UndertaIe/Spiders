# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
from random import choice
from settings import PROXY_EXPIRE
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from .utils.ProxyHandler import getProxy,getAllProxy


class ProxyMiddleware(HttpProxyMiddleware):

    def __init__(self):
        self.proxy = None
        self.proxies = None
        self.expire_datetime = datetime.now() - timedelta(seconds=PROXY_EXPIRE)

    '''获取IP'''
    def _getProxy(self):
        self.proxy = getProxy()

    '''获取所有代理IP'''
    def _getProxy(self):
        self.proxies = getAllProxy()

    '''经过proxy_expire时间更换IP'''
    def _check_proxy(self):
        if datetime.now() > self.expire_datetime:
            self._getProxy()

    '''中间件调用函数'''
    def process_request(self, request, spider):
        self._check_proxy()
        aproxy = choice(self.proxies)
        if self.proxy is not None:
            # request.meta['proxy'] = 'http://' + self.proxy['proxy']
            request.meta['proxy'] = 'http://' + aproxy['proxy']
        else:
            print("###[WARNING] ProxyMiddleware Proxy get ERROR. Using local IP...... ###")
