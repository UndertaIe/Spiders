# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
from settings import PROXY_EXPIRE
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from utils.ProxyHandler import getProxy

class ProxyMiddleware(HttpProxyMiddleware):

    def __init__(self):
        self.proxy = None
        self.expire_datetime = datetime.now() - timedelta(seconds=PROXY_EXPIRE)

    '''获取IP'''
    def _getProxy(self):
        self.proxy = getProxy()

    '''经过proxy_expire时间更换IP'''
    def _check_proxy(self):
        if datetime.now() > self.expire_datetime:
            self._getProxy()

    '''中间件调用函数'''
    def process_request(self, request, spider):
        self._check_proxy()
        if self.proxy is not None:
            request.meta['proxy'] = 'http://' + self.proxy['proxy']
        else:
            print("###[WARNING] Proxy get ERROR. Using local IP...... ###")
