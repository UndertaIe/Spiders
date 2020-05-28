# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector
from ..items import BossItem
from scrapy.loader import ItemLoader
import re
import random
from time import sleep
'''
Slave,解析当前页面并获取数据，初始化bossItem对象，在pipieline中持久化。

cli:    
    default:scrapy crawl slave -search="" single=False
            scrapy crawl slave 
            
    scrapy crawl bossDetail -a search=<优先搜索项> single=False 优先搜索search，结束后获取redis_key继续运行
    scrapy crawl bossDetail -a search=<优先搜索项> single=True 优先搜索search，运行结束后退出爬虫程序
    scrapy crawl bossDetail -a single=True  从redis获取一次redis_key，获取url直到无此redis_key无url后退出
    scrapy crawl bossDetail -a single=False 从redis获取redis_key，获取url直到无此redis_key时再次获取redis_key运行，直到没有符合条件的key后结束爬虫程序
 
'''
class BossDetailSpider(RedisSpider):
    #爬虫名
    name = "boss"
    #scrapy-redis启动请求
    redis_key = "Boss:{}:detail_urls"

    def __init__(self,search="",single=False,*args,**kwargs):
        super(BossDetailSpider, self).__init__(*args,**kwargs)

        self.search = search
        self.redis_key = self.redis_key.format(self.search)  # 生成第一个redis_key
        self.singleSearch = single
        print("###[INFO] Boss Detail Spider <{}> is running... ###".format(self.name))

    #从detail_urls拿到详情页面，得到搜集的数据。
    def parse(self, response):
        # detail selector
        #数据解析复杂 不适使用此种对象持久化方法
        # bossItem  = ItemLoader(item=BossItem, response=response)
        # bossItem.add_value()/add_xpath()/add_css()
        bossItem = BossItem()
        dSel = Selector(response=response)
        #工作类型
        job = self.getField(dSel,'//div[@class="info-primary"]/div[@class="name"]/h1/text()')
        #公司
        company = self.getField(dSel,'/html/body/div[1]/div[2]/div[3]/div/div[1]/div[2]/div/a[2]/text()')
        # 城市,经验，学历 该标签可能会出现四个
        cer = {'city':None,'exp':None,'requirement':None}  #对应 城市(city),经验(exp)，学历(requirement)
        try:
            three = dSel.xpath("/html/body/div[1]/div[2]/div[1]/div/div/div[2]/p/text()").extract()
            if len(three)==3:
                cer['city'] = three[0]
                cer['exp'] = three[1]
                cer['requirement'] = three[2]
            else:
                cer['city'] = three[0]
                cer['exp'] = three[2]
                cer['requirement'] = three[3] #防止出现四数据的情况
        except:
            cer['city'] =None
        # 薪资
        salary = self.getField(dSel,'//div[@class="name"]/span[@class="salary"]/text()')
        # 福利
        welfares = self.getField(dSel,'//*[@id="Task"]/div[1]/div/div/div[2]/div[3]/div[2]/span/text()')
        # 详细地址
        address = self.getField(dSel,'//*[@id="Task"]/div[3]/div/div[2]/div[2]/div/div[@class="job-location"]/div[@class="location-address"]/text()')
        # 岗位职责
        dutys = self.getField(dSel,'//*[@id="Task"]/div[3]/div/div[2]/div[2]/div[1]/div[@class="text"]/text()')
        # 发布时间
        try:
            publish = ''.join(re.findall('\d+.*', ''.join(dSel.xpath(
                '//*[@id="Task"]/div[3]/div/div[1]/div[2]/p[@class="gray"]/text()').extract()))).strip()
        except:
            publish = None
        # 详情链接:
        try:
            url = response.url
        except:
            url = None
        bossItem['search'] = self.search
        bossItem['job'] = job
        bossItem['company'] = company
        bossItem['city'] = cer['city']
        bossItem['exp'] = cer['exp']
        bossItem['requirement'] = cer['requirement']
        bossItem['salary'] = salary
        bossItem['welfares'] = welfares
        bossItem['address'] = address
        bossItem['dutys'] = dutys
        bossItem['publish'] = publish
        bossItem['url'] = url
        sleep(random.random())
        yield bossItem

    @staticmethod
    def getField(dSel, rule):
        try:
            result = ','.join(dSel.xpath(rule).extract()).strip()
        except:
            result = None
        return result