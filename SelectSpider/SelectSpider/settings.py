# -*- coding: utf-8 -*-

# Scrapy settings for DetailSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'SelectSpider'

SPIDER_MODULES = ['SelectSpider.spiders']
NEWSPIDER_MODULE = 'SelectSpider.spiders'

#=================================
#搜索工作类型
SITE = "Boss"
SEARCH = "{}:search".format(SITE)
SEARCH_TYPE="Jobs"
#=================================

#========================
#配置Redis数据库
#REDIS_HOST = "127.0.0.1" deprecated
#REDIS_PORT = 6379 deprecated
REDIS_PARAMS = {
    'host':'101.200.79.28',
    'port':6378,
    'password':'myredis0',
}
# REDIS_PARAMS = {
#     'host':'localhost',   #远程redis
#     'port':6379,
#     # 'password':'myredis0',
# }
#========================
#配置MongoDB数据库
MONGODB_HOST = "101.200.79.28"
MONGODB_PORT = 27016
MONGODB_DB = "{}{}".format(SITE, SEARCH_TYPE)
#========================
#配置代理服务
PROXY_URL = "http://101.200.79.28:5010/"
PROXY_METHOD = {"get":"get","get_all":"get_all","get_status":"get_status"}
PROXY_EXPIRE = 1 * 30 #经过30s更换代理 | 更换得到更新后的代理组并每个请求都更换代理
#========================
#配置Cookie
COOKIE_URL = "http://101.200.79.28:7788/"
COOKIE_METHOD = {"get":"get","count":"count"}

#是否开启Cookie
COOKIES_ENABLED = True
#是否遵循robots.txt
ROBOTSTXT_OBEY = False

#下载延迟
#DOWNLOAD_DELAY = 0
#并发请求个数
CONCURRENT_REQUESTS = 16

#下载中间件
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 550,
    'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 600,
    # 'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 610,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': None,
    # 'SelectSpider.ProxyMiddleware.ProxyMiddleware':101,
    # 'SelectSpider.CookieMiddleware.CookieMiddleware': 102,
    # 'SelectSpider.RotateUserAgentMiddleware.RotateUserAgentMiddleware':400,
    # 'SelectSpider.RedirectMiddleware.RedirectMiddleware':400,
    'SelectSpider.CookieProxyUserAgentBindMiddleware.CookieProxyUserAgentBindMiddleware':101,
    'SelectSpider.TimeoutMiddleware.TimeoutMiddleware':610,

}
#
# ITEM_PIPELINES = {
#     'SelectSpider.SelectPipelines.BossSelectPipeline': 300,
# }

LOG_LEVEL = 'WARNING'

REDIRECT_ENABLED = False
DOWNLOAD_TIMEOUT = 10
# Configure maximum concurrent requests performed by Scrapy (default: 16)


SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

MYEXT_ENABLED=True      # 开启扩展
IDLE_NUMBER=120           # 配置空闲持续时间单位为 120 ，一个时间单位为5s 超过这个时间 即10分钟空闲等待分布式爬虫自动关闭
RESET_KEY_NUMBER = 4     # 重置redis key时间片个数 超过这个时间 即20s空闲等待后重置redis_key 直到完成所有redis存储的select_urls模式的url

EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
    'SelectSpider.RedisSpiderExtensions.RedisSpiderExtension': 200,
}



# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
