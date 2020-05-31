#!/usr/bin/python
#-*-coding:utf-8-*-

from .utils.RedisHandler import RedisHandler
from scrapy.downloadermiddlewares.redirect import RedirectMiddleware

class Redirect_Middleware(RedirectMiddleware):

    def __init__(self, settings):
        super(Redirect_Middleware, self).__init__(settings)

    def process_response(self, request, response, spider):
        http_code = response.status
        search = spider.search
        if http_code // 100 == 2:
            #正常返回对应页面
            return response

        #处理请求失败 再次存入redis
        rhandler = RedisHandler()
        if http_code // 100 == 3 or http_code // 100 == 4:
            print("###[ERROR] RedirectMiddleware. Error Code: <{}> ###".format(http_code))
            flag = rhandler.insertDetailURL(search, request.url)
            if flag != 0:
                print('###[WARNING] RedirectMiddleware <{}> Detail URL : {} >>>> Redis <{}> detail_urls ###'.format(search, request.url,
                                                                                             search))
            else:
                print('###[ERROR] RedirectMiddleware <{}> Detail URL : {} |||| Redis <{}> detail_urls ###'.format(search, request.url,
                                                                                           search))
        rhandler.close()
        #
        # if http_code // 100 == 5:
        #     return request.replace(dont_filter=True)

        # # 获取重定向的url
        # url = response.headers['location']
        # domain = parse.urlunparse(url).netloc
        # if domain in spider.allowed_domains:
        #     return Request(url=url, meta=request.meta)
        # print('###[ERROR] response status 302 ###')
        # # 把request返回到下载器
        # return request.replace(dont_filter=True)