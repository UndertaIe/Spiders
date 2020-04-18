# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from scrapy.exceptions import DropItem
from .settings import MONGODB_IP,MONGODB_PORT,MONGODB_DB

class BossPipeline:
    mongodb_ip = MONGODB_IP
    mongodb_port = MONGODB_PORT
    mongodb_db = MONGODB_DB

    def __init__(self):
        #初始化mongodb连接
        try:
            client = MongoClient(self.mongodb_ip, self.mongodb_port)
            self.db = client[self.mongodb_db]
        except Exception:
            print("!!!MongoDB Connection Error!!!")

    @classmethod
    def from_crawler(cls, crawler):
        cls.MONGODB_SERVER = crawler.settings.get('MONGODB_IP', '127.0.0.1')
        cls.MONGODB_PORT = crawler.settings.getint('MONGODB_PORT', 27017)
        cls.MONGODB_DB = crawler.settings.get('MONGODB_DB', "Python")
        pipe = cls()
        pipe.crawler = crawler
        return pipe

    def process_item(self, item, spider):
        if item['job'] is None:
            raise DropItem("Duplicate item found: %s" % item)
        if item['company'] is None:
            raise DropItem("Duplicate item found: %s" % item)
        if item['city']is None:
            raise DropItem("Duplicate item found: %s" % item)
        if item['exp']is None:
            raise DropItem("Duplicate item found: %s" % item)
        if item['requirement'] is None:
            raise DropItem("Duplicate item found: %s" % item)
        if item['salary'] is None:
            raise DropItem("Duplicate item found: %s" % item)
        if item['welfares'] is None:
            raise DropItem("Duplicate item found: %s" % item)
        if item['address'] is None:
            raise DropItem("Duplicate item found: %s" % item)
        if item['dutys'] is None:
            raise DropItem("Duplicate item found: %s" % item)
        if item['publish'] is None:
            raise DropItem("Duplicate item found: %s" % item)
        if item['url'] is None:
            raise DropItem("Duplicate item found: %s" % item)
        bossItem = {
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
        col = bossItem['city'] #collection
        result = self.db.col.insert_one(bossItem)
        print('[success] the '+bossItem['detail']+'wrote to MongoDB database')
        return item
