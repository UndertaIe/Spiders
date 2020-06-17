# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from ..utils.RedisHandler import RedisHandler
from ..utils.prettyprint import printPretty
import re
from ..utils.SleepUtil import sleepRandom
from urllib.parse import unquote,urljoin
from time import sleep
import random
import sys
'''
mSlave:负责解析目录页，从而得到30详情页链接和下一页链接，前者存入detail_urls，后者存入select_urls

cli:    
    default:scrapy crawl mslave -search="" single=False
            scrapy crawl mslave 
            
    scrapy crawl bossSelect -a search=优先搜索项 single=False 优先搜索search，结束后获取redis_key继续运行
    scrapy crawl bossSelect -a search=优先搜索项 single=True 优先搜索search，运行结束后退出爬虫程序
    scrapy crawl bossSelect -a single=True 从redis获取一次redis_key，获取url直到无此redis_key无url后退出
    scrapy crawl bossSelect -a single=False从redis获取redis_key，获取url直到无此redis_key时再次获取redis_key运行，直到没有符合条件的key后结束爬虫程序
        
'''

class BossSelectSpider(RedisSpider):
    #爬虫名
    name = "boss"
    #scrapy-redis启动请求
    redis_key = "Boss:{}:select_urls"

    def __init__(self,search="",single="False",*args,**kwargs):
        super(BossSelectSpider, self).__init__(*args,**kwargs)

        # 搜索名
        self.search = search
        self.redis_key = self.redis_key.format(self.search)  # 生成第一个redis_key
        self.single = single != "False"
        self.redisHandler = RedisHandler()

        printPretty("###[INFO] Boss Select Spider <{}> is running... ###".format(self.name))

    #从select_urls拿到master搜索的得到的url，通过此url拿到下一页的url和此页面的工作详情url
    def parse(self, response):
        #精准搜索策略
        current_url = unquote(response.url)
        ma = re.search("query=(.*?)&", current_url)
        if ma is not None:
            city = ma.group(1)[len(self.search):]  #从当前URL获取城市名


        list_selector = Selector(response)
        base_url = "https://www.zhipin.com"
        # 获取当前页面所有的li标签，一个标签就是一条招聘数据
        error_select_count = 0  #此页面不匹配搜索的个数
        jobList = list_selector.xpath('/html/body/div[1]/div[3]/div/div[2]/ul/li').extract()
        for job_text in jobList:
            job_table =Selector(text=job_text)
            job_adrs = "".join(job_table.xpath('//span[@class="job-area"]/text()').extract()).strip()
            if job_adrs:  # 加这个判断是为了保证有城市数据，有时候网页会抽风导致 下标越界或空对象没有group()方法的错
                # 精准匹配:城市地点不符合搜索内容则过滤掉此页面
                # if (job_adrs[0]).find(city) == -1:
                if re.findall(city,job_adrs) is None:
                    error_select_count += 1
                    if error_select_count >= 5:  # 不匹配数据次数大于5次退出
                        print("###[INFO] No content match <{}> .Exit the current page ###".format(city))
                        break

                relative_url = ''.join(job_table.xpath(
                    '//div[@class="primary-box"]/@href').extract()).strip()
                #生成detail_url
                detail_url = urljoin(base_url, relative_url)

                flag = self.redisHandler.insertDetailURL(self.search, detail_url)

                if flag != 0:
                    mes = '###[SUCCESS] Select URL <{}> : {} >>> Redis <{}> detail_urls ###'.format(job_adrs, detail_url, self.search)
                    sys.stdout.write(mes + '\n')
                    sys.stdout.flush()
                else:
                    mes = '###[WARNING] Select URL <{}> : {} -|- Redis <{}> detail_urls ###'.format(job_adrs, detail_url, self.search)
                    sys.stdout.write(mes + '\n')
                    sys.stdout.flush()

        #准备获取下一页面  不符合搜索城市
        if len(jobList) == 30 and error_select_count<5:
            # 获取当前页面的下一页URL
            next_relative_url = "".join(list_selector.xpath('//a[@ka="page-next"]/@href').extract()).strip()
            if  next_relative_url != "javascript:;":
                next_select_url = urljoin(base_url,next_relative_url)
                # 获取当前页面的下一页URL
                self.redisHandler.insertSelectURL(self.search, next_select_url)
                print("###[SUCCESS] Search URL <{}> : {} >>> Redis <{}> select_urls ###".format(city,next_select_url,self.search))
            else:
                print("###[INFO] Search <{}> City <{}> all over #".format(self.search, city))
        else:
            print("###[INFO] Search <{}> City <{}> all over #".format(self.search, city))
