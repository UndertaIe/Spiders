# -*- coding: utf-8 -*-


from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from .utils.ProxyHandler import getProxy
from urllib.request import getproxies

class ProxyMiddleware(HttpProxyMiddleware):
    #此处可添加稳定高速的代理
    def __init__(self, auth_encoding='latin-1'):
        self.auth_encoding = auth_encoding
        self.proxies = {}
        for type_, url in getproxies().items():
            self.proxies[type_] = self._get_proxy(url, type_)

    def process_request(self, request, spider):
        proxy = getProxy()
        request.meta['proxy'] = 'http://' + proxy['proxy']
