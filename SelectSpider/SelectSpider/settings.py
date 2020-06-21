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
SEARCH_TYPE="Jobs"

SEARCH = "{}:search".format(SITE)
#=================================

#========================
#配置Redis数据库
#REDIS_HOST = "127.0.0.1" deprecated
#REDIS_PORT = 6379 deprecated
# REDIS_PARAMS = {
#     'host':'101.200.79.28',
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
MONGODB_DB = "{}{}".format(SITE, SEARCH_TYPE)

#========================

#配置代理服务
# PROXY_URL = "http://101.200.79.28:5010/"
# PROXY_METHOD = {"get":"get","get_all":"get_all","get_status":"get_status"}
# PROXY_EXPIRE = 1 * 30 #经过30s更换代理 | 更换得到更新后的代理组并每个请求都更换代理

PROXY_URL = "http://127.0.0.1:5010/"
PROXY_METHOD = {"get":"get", "get_charge":"get_charge", "get_all":"get_all", "get_status":"get_status"}
PROXY_EXPIRE = 1 * 30 #经过30s更换代理 | 更换得到更新后的代理组并每个请求都更换代理

#========================

#配置Cookie
# COOKIE_URL = "http://101.200.79.28:7788/"
# COOKIE_METHOD = {"get":"get","count":"count"}

COOKIE_URL = "http://127.0.0.1:7700/"
COOKIE_METHOD = {"get":"get","count":"count"}

#是否开启Cookie
COOKIES_ENABLED = True
#是否遵循robots.txt
ROBOTSTXT_OBEY = False

#下载延迟 测试不是用代理 并发请求数较低
DOWNLOAD_DELAY = 4

#并发请求个数  测试不使用代理 并发请求数较低
CONCURRENT_REQUESTS = 2

#是否运行重定向 这里设置False 因为cookiepool已经完成了cookie的认证。携带cookie访问不需要重定向。
REDIRECT_ENABLED = False
DOWNLOAD_TIMEOUT = 5

HTTPERROR_ALLOWED_CODES = [403,302,304,307,404]

#redis存储 set类型
REDIS_START_URLS_AS_SET = True

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
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware':None,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': None,
    # 'SelectSpider.ProxyMiddleware.ProxyMiddleware':101,
    # 'SelectSpider.CookieMiddleware.CookieMiddleware': 102,
    # 'SelectSpider.UserAgentMiddleware.RotateUserAgentMiddleware':400,
    'SelectSpider.RedirectMiddleware.Redirect_Middleware':400,
    'SelectSpider.CookieProxyUserAgentBindMiddleware.CookieProxyUserAgentBindMiddleware':101,
    'SelectSpider.TimeoutMiddleware.TimeoutMiddleware':610,

}
#
ITEM_PIPELINES = {
    'SelectSpider.SelectPipelines.BossSelectPipeline': 300,
}

LOG_LEVEL = 'INFO'

# Configure maximum concurrent requests performed by Scrapy (default: 16)


SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

REDIS_EXT_ENABLED=True      # 开启扩展
IDLE_NUMBER=8           # 配置空闲次数为8，超过该次数，表示redis中无符合筛选条件的key值 结束爬虫程序
RESET_KEY_NUMBER = 3     # 重置redis key的idle次数。超过该次数，表示空闲次数满足重置redis key的条件，重置redis key

EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
    'SelectSpider.RedisSpiderExtensions.RedisSpiderExtension': 1,
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
