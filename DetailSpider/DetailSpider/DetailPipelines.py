# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from scrapy.exceptions import DropItem
from .settings import MONGODB_HOST,MONGODB_PORT,MONGODB_DB

class BossDetailPipeline:

    def __init__(self):
        #初始化mongodb连接
        try:
            client = MongoClient(MONGODB_HOST, MONGODB_PORT)
            self.db = client[MONGODB_DB]
        except Exception:
            print("###[ERROR] MongoDB Connection Error ###")

    @classmethod
    def from_crawler(cls, crawler):
        cls.MONGODB_SERVER = crawler.settings.get('MONGODB_IP', '127.0.0.1')
        cls.MONGODB_PORT = crawler.settings.getint('MONGODB_PORT', 27017)
        cls.MONGODB_DB = crawler.settings.get('MONGODB_DB', "BossJobs")
        pipe = cls()
        pipe.crawler = crawler
        return pipe

    def process_item(self, item, spider):
        if item['search'] is None:
            raise DropItem("Duplicate item found: search is None")
        if item['job'] is None:
            raise DropItem("Duplicate item found: job is None")
        if item['company'] is None:
            raise DropItem("Duplicate item found: company is None")
        if item['city']is None:
            raise DropItem("Duplicate item found: city is None")
        if item['exp']is None:
            raise DropItem("Duplicate item found: exp is None")
        if item['requirement'] is None:
            raise DropItem("Duplicate item found: requirement is None")
        if item['salary'] is None:
            raise DropItem("Duplicate item found: salary is None")
        if item['welfares'] is None:
            raise DropItem("Duplicate item found: welfares is None")
        if item['address'] is None:
            raise DropItem("Duplicate item found: address is None")
        if item['dutys'] is None:
            raise DropItem("Duplicate item found: dutys is None")
        #if item['publish'] is None:
        #    raise DropItem("Duplicate item found: pubilish is None")
        if item['url'] is None:
            raise DropItem("Duplicate item found: url is None")
        aItem = {
            'search': item.get('search'),
            'job': item.get('job'),
            'company': item.get('company'),
            'city': item.get('city'),
            'exp': item.get('exp'),
            'requirement': item.get('requirement', ''),
            'salary': item.get('salary'),
            'welfares': item.get('welfares', ''),
            'address': item.get('address', ''),
            'dutys': item.get('dutys', ''),
            'publish': item.get('publish', ''),
            'url': item.get('url', '')
        }
        #将一条数据写入mongodb
        col = aItem['search']
        result = self.db[col].insert_one(aItem)
        if result is not None:
            print('###[SUCCESS] the {} Item >>> MongoDB {} Collection ###'.format(aItem['url'], col))
        else:
            print('###[WARNING] the {} Item -|- MongoDB {} Collection ###'.format(aItem['url'], col))
        #不显示到屏幕
        #return item
