#!/usr/bin/python 
# -*- coding: utf-8 -*-

import re
import sys
import requests
from time import sleep
from scrapy.selector import Selector
sys.path.append('..')

from Util.WebRequest import WebRequest
from Util.utilFunction import getHtmlTree

# for debug to disable insecureWarning
requests.packages.urllib3.disable_warnings()

class GetChargeProxy(object):
    """
    get charge Proxy 此类添加收费代理，添加后需在setting中注册代理方法
    """
    @staticmethod
    def chargeProxy01():
        """
            芝麻代理 高效稳定   收费
        """
        # zhima_url = ""
        # request = WebRequest()
        # res = request.get(zhima_url,timeout=10)
        # j = res.json()
        # if j.get('code') == 0:
        #     proxy_list = j.get('data')
        #     for l in proxy_list:
        #         proxy = "{ip}:{port}".format(ip=l.get('ip'),port=l.get('port'))
        #         yield proxy
        pass

    @staticmethod
    def chargeProxy02():
        pass
