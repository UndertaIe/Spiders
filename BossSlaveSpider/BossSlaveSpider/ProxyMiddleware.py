# -*- coding: utf-8 -*-


from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from .utils.ProxyHandler import getProxy

class ProxyMiddleware(HttpProxyMiddleware):
    def __init__(self):
        pass
    def process_request(self, request, spider):
        aproxy = getProxy()
        request.meta['proxy'] = 'http://' + aproxy['proxy']
