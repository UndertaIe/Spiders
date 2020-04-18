# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from ..utils.RedisHandler import RedisHandler
import re
from urllib.parse import unquote,urljoin
from ..settings import RESARCH_NAME
from time import sleep
import random
'''
mSlave:负责解析目录页，从而得到30详情页链接和下一页链接，前者存入detail_urls，后者存入select_urls
'''
class BossSpider(RedisSpider):
    #爬虫名
    name = "mslave"
    #scrapy-redis启动请求
    redis_key = "Boss:{}:select_urls".format(RESARCH_NAME)
    def __init__(self):
        super(BossSpider, self).__init__()
        self.redisHandler = RedisHandler()

    #从select_urls拿到master搜索的得到的url，通过此url拿到下一页的url和此页面的工作详情url
    def parse(self, response):
        # 当前中文url
        current_url = unquote(response.url)
        ma = re.search("query=(.*?)&", current_url)
        if ma is not None:
            city = ma.group(1)[len(RESARCH_NAME):]
        list_selector = Selector(response)
        base_url = "https://www.zhipin.com"
        # 获取当前页面所有的li标签，一个标签就是一条招聘数据
        jobList = list_selector.xpath('/html/body/div[1]/div[3]/div/div[2]/ul/li').extract()
        for job_text in jobList:
            job_table =Selector(text=job_text)
            job_adrs = job_table.xpath('//span[@class="job-area"]/text()').extract()
            if job_adrs:  # 加这个判断是为了保证有城市数据，有时候网页会抽风导致 下标越界或空对象没有group()方法的错
                # 精准匹配:城市地点不符合搜索内容则过滤掉此页面
                if (job_adrs[0]).find(city) == -1:
                    continue
                relative_url = ''.join(job_table.xpath(
                    '//div[@class="primary-box"]/@href').extract()).strip()

                detail_url = urljoin(base_url, relative_url)
                self.redisHandler.insertDetailURL(detail_url)

        if len(jobList) == 30:
            print("开始下次解析")
            # 获取当前页面的下一页URL
            next_relative_url = "".join(list_selector.xpath('//a[@ka="page-next"]/@href').extract()).strip()
            if  next_relative_url != "javascript:;":
                next_select_url = urljoin(base_url,next_relative_url)
                # 获取当前页面的下一页URL
                self.redisHandler.insertSelectURL(next_select_url)
            else:
                print("此地区查询已结束")
        else:
            print("此地区查询已结束")
        sleep(random.randint(1,3))
