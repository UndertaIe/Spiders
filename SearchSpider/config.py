#!/usr/bin/python 
# -*- coding: utf-8 -*-

#===============================
#搜索项key 通过redis key获取搜索项
SEARCH = "Boss:search"
#===============================

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
    'host':'127.0.0.1',
    'port':6379,
    'password':'myredis0',
}

#========================

#========================
#配置代理服务
# PROXY_URL = "http://101.200.79.28:5010/"
PROXY_URL = "http://127.0.0.1:5010/"
PROXY_METHOD = {"get":"get","get_all":"get_all","get_status":"get_status"}
PROXY_EXPIRE = 1 * 30
#========================

# CHROMEDRIVERPATH = "chromedriver.exe"
# FIREFOXDRIVERPATH="geckodriver.exe"
# PHANTOMJSPATH="phantomjs.exe"
HOTCITY = True
hotCitys = ['北京', '上海', '广州', '深圳', '杭州', '天津', '西安', '苏州', '武汉', '厦门', '长沙', '成都', '郑州', '重庆']

HEADERS = '''
        +------------------------+
        |    BossSearchSPider    |
        +------------------------+
    '''

