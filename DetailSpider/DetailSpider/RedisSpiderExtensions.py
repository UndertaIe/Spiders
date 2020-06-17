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
        self.reset_key_number =  reset_key_number
        self.idle_number = idle_number
        self.idle_list = []  # 记录大于5s的idle列表，超过规定次数，结束爬虫程序
        self.idle_count = 0  # 记录大于5s的idle次数，超过规定次数，更换reids key
        self.rhandler = RedisHandler()
    @classmethod
    def from_crawler(cls, crawler):
        # 首先检查是否应该启用和提高扩展
        # 否则不配置
        if not crawler.settings.getbool('REDIS_EXT_ENABLED'):
            raise NotConfigured

        # 获取配置中的时间片个数，默认为4个，即20s空闲则重置redis_key
        reset_key_number = crawler.settings.getint("RESET_KEY_NUMBER", 4)
        # 获取配置中的时间片个数，默认为360个，30分钟
        idle_number = crawler.settings.getint('IDLE_NUMBER', 120)

        # 实例化扩展对象
        ext = cls(reset_key_number,idle_number, crawler)

        # 将扩展对象连接到信号， 将signals.spider_idle 与 spider_idle() 方法关联起来。
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.spider_idle, signal=signals.spider_idle)

        # return the extension object
        return ext

    def spider_opened(self, spider):
        if spider.search == "":
            logger.info("###[INFO] RedisSpider without cli search arg, get detail_urls from Redis ###")
            key = self.rhandler.get_redis_detail_key()
            if key is not None:
                spider.redis_key = key  # 更换redis_key
                spider.search = key.split(":")[1]  # 更换spider search
        logger.info("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
        logger.info("###[INFO] RedisSpider current redis_key: <{}>, search: <{}> ###".format(spider.redis_key,spider.search))
        logger.info("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")

    def spider_closed(self, spider):
        logger.info("###[INFO] RedisSpider <{}> close, idle count {} , Continuous idle count {} ###".format(spider.name, self.idle_count, len(self.idle_list)))

    #下载空闲时会调用此方法
    def spider_idle(self, spider):
        self.idle_list.append(time.time())  # 每次触发 spider_idle 空闲时，记录下触发时间戳
        idle_list_len = len(self.idle_list)  # 获取当前已经连续触发的次数

        # 表示此时已经进入redis key无url的idle状态，此状态下不清空空闲列表idle_list 并且空闲次数加1，到达一定数目进行更改key的判断。
        if idle_list_len > 1 and self.idle_list[-1] - self.idle_list[-2] < 6:  # scrapy 队列为空时idle间隔大约5s上下
            self.idle_count += 1
        # 表示此时请求间隔大于5s即redis key中仍有url可被获取.然后空闲计数器归零，空闲列表记录当前时间戳。
        else:
            self.idle_count = 0
            self.idle_list = [self.idle_list[-1]]

        # 空闲数目大于重置redis key的idle次数 并小于退出爬虫的idle次数的状态下 若存在符合条件的Redis key重置 key
        if self.reset_key_number < self.idle_count < self.idle_number and not spider.single:
            self.idle_count = 0  # 归零
            if self.rhandler.get_current_redis_key_len(spider.redis_key) == 0:
                key = self.rhandler.get_redis_detail_key()
                if key is not None:
                    spider.redis_key = key  # 更换redis_key
                    spider.search = key.split(":")[1]  # 更换spider search
                    logger.info("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
                    logger.info("###[INFO] RedisSpider current redis_key: <{}>. Search: <{}> ###".format(spider.redis_key, spider.search))
                    logger.info("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
                    self.idle_list.clear()
                    
        if idle_list_len > self.idle_number:
            self.idle_list.clear()
            if self.rhandler.get_current_redis_key_len(spider.redis_key) == 0:
                # 执行关闭爬虫操作
                self.rhandler.close()
                self.crawler.engine.close_spider(spider, 'DetailSpider')

