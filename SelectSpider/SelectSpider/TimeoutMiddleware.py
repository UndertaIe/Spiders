# -*- coding: utf-8 -*-

from scrapy.downloadermiddlewares.downloadtimeout import DownloadTimeoutMiddleware
from time import sleep
from .utils.RedisHandler import RedisHandler
from scrapy import signals


class TimeoutMiddleware(DownloadTimeoutMiddleware):

    def process_exception(self,request, exception, spider):
        # print("###[WARNING] TimeoutMiddleware TimeoutException ###")
        # sleep(3)
        r = RedisHandler()
        flag = r.insertSelectURL(spider.search,request.url)
        if flag != 0:
            print('###[INFO] TimeoutMiddleware  {} Select URL : {} >>>> Redis {} select_urls ###'.format(spider.search, request.url, spider.search))
        else:
            print('###[ERROR] TimeoutMiddleware {} Select URL : {} |||| Redis {} select_urls ###'.format(spider.search, request.url,
                                                                                         spider.search))