# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#Boss爬取信息

class BossItem(scrapy.Item):
    # define the fields for your item here like:
    job = scrapy.Field() #职位
    company = scrapy.Field() #公司
    city = scrapy.Field() #城市
    exp = scrapy.Field() #工作经验
    requirement = scrapy.Field()  # 学历
    salary = scrapy.Field() #薪资
    welfares = scrapy.Field() #福利
    dutys = scrapy.Field() #岗位职责
    publish = scrapy.Field() #发布时间
    address = scrapy.Field # 详细地址
    url = scrapy.Field() #细节链接页面
