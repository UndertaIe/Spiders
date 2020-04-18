# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector
from ..items import BossItem
from scrapy.loader import ItemLoader
import re
from ..settings import RESARCH_NAME
import random
from time import sleep
'''
Slave
'''
class BossSpider(RedisSpider):
    #爬虫名
    name = "slave"
    #scrapy-redis启动请求
    redis_key = "Boss:{}:detail_urls".format(RESARCH_NAME)
    def __init__(self):
        super(BossSpider, self).__init__()
    #从detail_urls拿到详情页面，得到搜集的数据。
    def parse(self, response):
        # detail selector
        #bossItem  = ItemLoader(item=BossItem, response=response)
        bossItem = BossItem()
        dSel = Selector(response=response)
        #工作类型
        job = self.getField(dSel,'//div[@class="info-primary"]/div[@class="name"]/h1/text()')
        #公司
        company = self.getField(dSel,'/html/body/div[1]/div[2]/div[3]/div/div[1]/div[2]/div/a[2]/text()')
        # 城市,经验，学历 该标签可能会出现四个
        cer = {} #对应 城市(city),经验(exp)，学历(requirement)
        try:
            three = dSel.xpath("/html/body/div[1]/div[2]/div[1]/div/div/div[2]/p/text()").extract()
            if len(three)==3:
                cer.setdefault('city',three[0],None)
                cer.setdefault('exp', three[1], None)
                cer.setdefault('city', three[2], None)
            elif len(three)==4:
                cer.setdefault('city', three[0], None)
                cer.setdefault('exp', three[2], None)
                cer.setdefault('city', three[3], None)
            else:
                raise TypeError
        except:
            cer.setdefault('city',None)
        # 薪资
        salary = self.getField(dSel,'//div[@class="name"]/span[@class="salary"]/text()')
        # 福利
        welfares = self.getField(dSel,'//*[@id="main"]/div[1]/div/div/div[2]/div[3]/div[2]/span/text()')
        # 详细地址
        address = self.getField(dSel,'//*[@id="main"]/div[3]/div/div[2]/div[2]/div/div[@class="job-location"]/div[@class="location-address"]/text()')
        # 岗位职责
        dutys = self.getField(dSel,'//*[@id="main"]/div[3]/div/div[2]/div[2]/div[1]/div[@class="text"]/text()')
        # 发布时间
        try:
            publish = ''.join(re.findall('\d+.*', ''.join(dSel.xpath(
                '//*[@id="main"]/div[3]/div/div[1]/div[2]/p[@class="gray"]/text()').extract()))).strip()
        except:
            publish = None
        # 详情链接:
        try:
            url = response.url
        except:
            url = None
        bossItem['job'] = job
        bossItem['company'] = company
        bossItem['city'] = cer[0]
        bossItem['exp'] = cer[1]
        bossItem['requirement'] = cer[2]
        bossItem['salary'] = salary
        bossItem['welfares'] = welfares
        bossItem['address'] = address
        bossItem['dutys'] = dutys
        bossItem['publish'] = publish
        bossItem['url'] = url
        sleep(random.randint(1,3))
        yield bossItem

    @staticmethod
    def getField(dSel, rule):
        try:
            result = ','.join(dSel.xpath(rule).extract()).strip()
        except:
            result = None
        return result