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
SEARCH_TYPE="Jobs"

SEARCH = "{}:search".format(SITE)

#=================================

#========================

#配置Redis数据库
#REDIS_HOST = "127.0.0.1" deprecated
#REDIS_PORT = 6379 deprecated
# REDIS_PARAMS = {
#     'host':'101.200.79.28',   #远程redis
#     'port':6378,
#     'password':'myredis0',
# }

REDIS_PARAMS = {
    'host':'localhost',   #远程redis
    'port':6379,
    'password':'myredis0',
}
#========================
#配置MongoDB数据库
# MONGODB_HOST = "101.200.79.28"
# MONGODB_PORT = 27016
# MONGODB_DB = "{}{}".format(SITE, SEARCH_TYPE)

MONGODB_HOST = "127.0.0.1"
MONGODB_PORT = 27017
MONGODB_DB = "{}{}".format(SITE, SEARCH_TYPE) #可在此修改 自定义存储数据库名 默认为SITE+SEARCH_TYPE
#========================
#配置代理服务
# PROXY_URL = "http://101.200.79.28:5010/"
# PROXY_METHOD = {"get":"get","get_all":"get_all","get_status":"get_status"}
# PROXY_EXPIRE = 1 * 30 #代理使用时间即经过30s更换代理

PROXY_URL = "http://127.0.0.1:5010/"
PROXY_METHOD = {"get":"get", "get_charge":"get_charge", "get_all":"get_all", "get_status":"get_status"}
PROXY_EXPIRE = 1 * 30 #代理使用时间即经过30s更换代理
#========================
#配置Cookie
# COOKIE_URL = "http://101.200.79.28:7700/"
# COOKIE_METHOD = {"get":"get","count":"count"}

COOKIE_URL = "http://127.0.0.1:7700/"
COOKIE_METHOD = {"get":"get","count":"count"}

#是否开启Cookie
COOKIES_ENABLED = True
#是否遵循robots.txt
ROBOTSTXT_OBEY = False

#下载延迟 测试不是用代理 当前并发请求数设置较低
# DOWNLOAD_DELAY = 2
#并发请求个数  测试不使用代理 并发请求数较低
CONCURRENT_REQUESTS = 2

#是否运行重定向 这里设置False 因为cookiepool已经完成了cookie的认证。携带cookie访问不需要重定向。
REDIRECT_ENABLED = False

DOWNLOAD_TIMEOUT = 5

HTTPERROR_ALLOWED_CODES = [403,302,304,307,404]

#redis存储set类型
REDIS_START_URLS_AS_SET = True

#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

#下载中间件
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 550,
    'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': None,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware':None,
    # 'DetailSpider.ProxyMiddleware.ProxyMiddleware':101,
    # 'DetailSpider.CookieMiddleware.CookieMiddleware': 102,
    # 'DetailSpider.UserAgentMiddleware.RotateUserAgentMiddleware':400,
    'DetailSpider.CookieProxyUserAgentBindMiddleware.CookieProxyUserAgentBindMiddleware':101,
    'DetailSpider.RedirectMiddleware.Redirect_Middleware':400,
    'DetailSpider.TimeoutMiddleware.TimeoutMiddleware':610,

}

ITEM_PIPELINES = {
    'DetailSpider.DetailPipelines.BossDetailPipeline': 300,
}

LOG_LEVEL = 'INFO'


# Configure maximum concurrent requests performed by Scrapy (default: 16)


# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# The download delay setting will honor only one of:

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"


REDIS_EXT_ENABLED=True      # 开启扩展
IDLE_NUMBER=8           # 配置空闲次数为8，超过该次数，表示redis中无符合筛选条件的key值 结束爬虫程序
RESET_KEY_NUMBER = 3    # 重置redis key的idle次数。超过该次数，表示空闲次数满足重置redis key的条件，重置redis key

EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
    'DetailSpider.RedisSpiderExtensions.RedisSpiderExtension': 500,
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
