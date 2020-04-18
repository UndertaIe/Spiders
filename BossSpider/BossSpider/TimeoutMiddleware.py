# -*- coding: utf-8 -*-

from scrapy.downloadermiddlewares.downloadtimeout import DownloadTimeoutMiddleware

class TimeoutMiddleware(DownloadTimeoutMiddleware):
    def process_exception(self,request, exception, spider):
        #print "####the downloader has exception!"
        print("!!!Timeout Exception!!!")
        return request.replace(dont_filter=True)
