# -*- coding: utf-8 -*-

# Scrapy settings for DetailSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'DetailSpider'

SPIDER_MODULES = ['DetailSpider.spiders']
NEWSPIDER_MODULE = 'DetailSpider.spiders'

#=================================
#第一个爬虫需要的redis key 可在RedisHandler中分解为如Boss:search:select_urls/detail_urls
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
#========================
#配置MongoDB数据库
MONGODB_HOST = "101.200.79.28"
MONGODB_PORT = 27016
MONGODB_DB = "{}{}".format(SITE, SEARCH_TYPE)
#========================
#配置代理服务
PROXY_URL = "http://101.200.79.28:5010/"
PROXY_METHOD = {"get":"get","get_all":"get_all","get_status":"get_status"}
PROXY_EXPIRE = 1 * 30 #代理使用时间即经过30s更换代理
#========================
#配置Cookie
COOKIE_URL = "http://101.200.79.28:7788/"
COOKIE_METHOD = {"get":"get","count":"count"}

#是否开启Cookie
COOKIES_ENABLED = True
#是否遵循robots.txt
ROBOTSTXT_OBEY = False

#DOWNLOAD_DELAY = 0
CONCURRENT_REQUESTS = 16

#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

#下载中间件
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 550,
    'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
    'scrapy.downloadermiddlewares.chunked.ChunkedTransferMiddleware': 830,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 400,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': None,
    'DetailSpider.ProxyMiddleware.ProxyMiddleware':101,
    'DetailSpider.CookieMiddleware.CookieMiddleware': 102,
    'DetailSpider.RotateUserAgentMiddleware.RotateUserAgentMiddleware':400,
    'DetailSpider.RedirectMiddleware.RedirectMiddleware':500,
    'DetailSpider.TimeoutMiddleware.TimeoutMiddleware':610,

}

ITEM_PIPELINES = {
    'DetailSpider.DetailPipelines.BossDetailPipeline': 300,
}

LOG_LEVEL = 'WARNING'


# Configure maximum concurrent requests performed by Scrapy (default: 16)


# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# The download delay setting will honor only one of:

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"


MYEXT_ENABLED=True      # 开启扩展
IDLE_NUMBER=120           # 配置空闲持续时间单位为 120 ，一个时间单位为5s 超过这个时间 即10分钟空闲等待分布式爬虫自动关闭
RESET_KEY_NUMBER = 4     # 重置redis key时间片个数 超过这个时间 即20s空闲等待后重置redis_key 直到完成所有redis存储的select_urls模式的url

EXTENSIONS = {
   'scrapy.extensions.telnet.TelnetConsole': None,
    'DetailSpider.extensions.RedisSpiderSmartIdleClosedExtensions': 500,
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'DetailSpider.pipelines.BossslavespiderPipeline': 300,
#}

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
