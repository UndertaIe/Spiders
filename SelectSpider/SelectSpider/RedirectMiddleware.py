#!/usr/bin/python
#-*-coding:utf-8-*-

from utils.RedisHandler import RedisHandler
from scrapy.downloadermiddlewares.redirect import RedirectMiddleware

class Redirect_Middleware(RedirectMiddleware):

    def __init__(self, settings):
        super(Redirect_Middleware, self).__init__(settings)

    def process_response(self, request, response, spider):
        http_code = response.status
        search = spider.search
        if http_code // 100 == 2:
            # 正常返回对应页面
            return response

        # 处理请求失败 再次存入redis
        rhandler = RedisHandler()
        if http_code // 100 == 3 or http_code // 100 == 4:
            print("###[ERROR] Spider Request returned abnormal page.Error Code: {} ###".format(http_code))
            flag = rhandler.insertSelectURL(search, request.url)
            if flag != 0:
                print('###[SUCCESS] Select URL {} : {} >>>> Redis {} select_urls ###'.format(search, request.url,
                                                                                             search))
            else:
                print('###[ERROR] Select URL {} : {} |||| Redis {} select_urls ###'.format(search, request.url,
                                                                                           search))
        rhandler.close()
        #
        # if http_code // 100 == 5:
        #     return request.replace(dont_filter=True)

        # # 对于重定向正确页面的url可以采取重新导入redis获取重定向的url，若重定向为验证页面则不插入redis
        # url = response.headers['location']
        # domain = parse.urlunparse(url).netloc
        # if domain in spider.allowed_domains:
        #     return Request(url=url, meta=request.meta)
        # print('###[ERROR] response status 302 ###')
        # # 把request返回到下载器
        # return request.replace(dont_filter=True)