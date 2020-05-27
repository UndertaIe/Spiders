# -*- coding: utf-8 -*-

from scrapy.downloadermiddlewares.downloadtimeout import DownloadTimeoutMiddleware
from time import sleep
from .utils.RedisHandler import RedisHandler

class TimeoutMiddleware(DownloadTimeoutMiddleware):
    def process_exception(self,request, exception, spider):
        #print "####the downloader has exception!"
        # print("###[WARNING] Spider Request timeout Exception ###")
        # sleep(3)
        r = RedisHandler()
        flag = r.insertDetailURL(spider.search, request.url)
        if flag != 0:
            print('###[INFO] Timeout {} Detail URL : {} >>>> Redis {} detail_urls ###'.format(spider.search, request.url,
                                                                                         spider.search))
        else:
            print('###[ERROR] Timeout {} Detail URL : {} |||| Redis {} detail_urls ###'.format(spider.search, request.url,
                                                                                       spider.search))
