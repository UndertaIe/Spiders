# -*- coding: utf-8 -*-
# Define here the models for your scraped Extensions
import logging
import time
from scrapy import signals
from scrapy.exceptions import NotConfigured
from .utils.RedisHandler import RedisHandler

logger = logging.getLogger(__name__)

class RedisSpiderExtension(object):

    def __init__(self, reset_key_number, idle_number, crawler):
        self.crawler = crawler
        self.reset_key_number = reset_key_number
        self.idle_number = idle_number
        self.idle_list = []
        self.idle_count = 0
        self.rhandler = RedisHandler()
    @classmethod
    def from_crawler(cls, crawler):
        # 首先检查是否应该启用和提高扩展
        # 否则不配置
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured

        # 获取配置中的时间片个数，默认为4个，即20s空闲则重置redis_key
        reset_key_number = crawler.settings.getint("RESET_KEY_NUMBER", 4)
        # 获取配置中的时间片个数，默认为360个，30分钟
        idle_number = crawler.settings.getint('IDLE_NUMBER', 120)

        # 实例化扩展对象
        ext = cls(reset_key_number, idle_number, crawler)

        # 将扩展对象连接到信号， 将signals.spider_idle 与 spider_idle() 方法关联起来。
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.spider_idle, signal=signals.spider_idle)

        # return the extension object
        return ext

    def spider_opened(self, spider):
        if spider.search == "":
            logger.info("###[INFO] RedisSpider without cli search arg, get select_urls from Redis ###")
            key = self.rhandler.get_redis_select_key()
            if key is not None:
                spider.redis_key = key  # 更换redis_key
                spider.search = key.split(":")[1]  # 更换spider search
        logger.info("###[INFO] RedisSpider current redis_key: <{}>, Search: <{}> ###".format(spider.redis_key, spider.search))

    def spider_closed(self, spider):
        logger.info("###[INFO] RedisSpider <{}> close, idle count {} , Continuous idle count {} ###".format(spider.name, self.idle_count, len(self.idle_list)))

    def spider_idle(self, spider):
        self.idle_count += 1  # 空闲计数
        self.idle_list.append(time.time())  # 每次触发 spider_idle 空闲时，记录下触发时间戳
        idle_list_len = len(self.idle_list)  # 获取当前已经连续触发的次数

            # 判断 当前触发时间与上次触发时间 之间的间隔是否大于5秒，如果大于5秒，说明redis 中还有key
        if idle_list_len > 1 and self.idle_list[-1] - self.idle_list[-2] > 6:
            self.idle_list = [self.idle_list[-1]] #重置idle_list
            # 连续空闲次数超过设置的reset_key_number并且singleSearch为False时则重置redis_key
        elif self.reset_key_number < idle_list_len < self.idle_number and ~spider.singleSearch:
            # 连续空闲触发的次数达到配置次数后更换redis_key
            key = self.rhandler.get_redis_select_key()
            if key is not None:
                spider.redis_key = key  # 更换redis_key
                spider.search = key.split(":")[1]  # 更换spider search
                logger.info("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
                logger.info("###[INFO] RedisSpider current redis_key: <{}>, Search: <{}> ###".format(spider.redis_key,spider.search))
                logger.info("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
        elif idle_list_len > self.idle_number:
            # 执行关闭爬虫操作
            self.rhandler.close()
            self.crawler.engine.close_spider(spider, 'SelectSpider')