# -*- coding: utf-8 -*-

# Scrapy settings for BossSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'BossSpider'

SPIDER_MODULES = ['BossSpider.spiders']
NEWSPIDER_MODULE = 'BossSpider.spiders'

#===============================
#搜索工作类型
RESARCH_NAME = "Python"
#===============================

#========================
#配置Redis数据库
REDIS_IP = "127.0.0.1"
REDIS_PORT = 6379
#========================
#配置MongoDB数据库
MONGODB_IP = "127.0.0.1"
MONGODB_PORT = 27017
MONGODB_DB = RESARCH_NAME
#========================
#配置代理服务
PROXY_URL = "http://127.0.0.1:5010/"
PROXY_METHOD = {"get":"get","get_all":"get_all","get_status":"get_status"}
#========================
#配置Cookie
COOKIE_URL = "http://127.0.0.1:7788/"
COOKIE_METHOD = {"get":"get","count":"count"}

#是否开启Cookie
COOKIES_ENABLED = True
#是否遵循robots.txt
ROBOTSTXT_OBEY = False

DOWNLOADER_MIDDLEWARES = {

    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 550,
    'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
    'scrapy.downloadermiddlewares.chunked.ChunkedTransferMiddleware': 830,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': None,
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 400,
    #'BossSpider.ProxyMiddleware.ProxyMiddleware':101, #代理
    'BossSpider.CookieMiddleware.CookieMiddleware': 102,
    'BossSpider.TimeoutMiddleware.TimeoutMiddleware':610, #超时
    'BossSpider.RotateUserAgentMiddleware.RotateUserAgentMiddleware':400, #UserAgent
    'BossSpider.RedirectMiddleware.RedirectMiddleware':500, # 重定向

}

ITEM_PIPELINES = {
    'BossSpider.BossPipelines.BossPipeline': 300,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#远程控制
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html


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
