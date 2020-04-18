#!/usr/bin/python
#-*-coding:utf-8-*-

from scrapy.exceptions import IgnoreRequest
from scrapy.exceptions import CloseSpider
from scrapy.http import Request
from urllib import parse
from scrapy.downloadermiddlewares.redirect import RedirectMiddleware

class Redirect_Middleware(RedirectMiddleware):

    def process_response(self, request, response, spider):
        http_code = response.status
        if http_code // 100 == 2:
            return response

        if http_code // 100 == 3 and http_code != 304:
            # 获取重定向的url
            url = response.headers['location']
            domain = parse.urlunparse(url).netloc
            if domain in spider.allowed_domains:
                return Request(url=url, meta=request.meta)
            print('302')
            # 把request返回到下载器
            return request.replace(dont_filter=True)
        if http_code // 100 == 4:
            # 需要注意403不是响应错误，是无权访问
            raise IgnoreRequest(u'404')

        if http_code // 100 == 5:
            return request.replace(dont_filter=True)
