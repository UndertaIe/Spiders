# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     utilFunction.py
   Description :  tool function
   Author :       JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: 添加robustCrawl、verifyProxy、getHtmlTree
-------------------------------------------------
"""
import requests
from lxml import etree

from Util.WebRequest import WebRequest


def robustCrawl(func):
    def decorate(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            pass
            # logger.info(u"sorry, 抓取出错。错误原因:")
            # logger.info(e)

    return decorate


def verifyProxyFormat(proxy):
    """
    检查代理格式
    :param proxy:
    :return:
    """
    import re
    verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
    _proxy = re.findall(verify_regex, proxy)
    return True if len(_proxy) == 1 and _proxy[0] == proxy else False


def getHtmlTree(url, **kwargs):
    """
    获取html树
    :param url:
    :param kwargs:
    :return:
    """

    header = {'Connection': 'keep-alive',
              'Cache-Control': 'max-age=0',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, sdch',
              'Accept-Language': 'zh-CN,zh;q=0.8',
              }
    # TODO 取代理服务器用代理服务器访问
    wr = WebRequest()
    html = wr.get(url=url, header=header,timeout=10).content
    return etree.HTML(html)


def tcpConnect(proxy):
    """
    TCP 三次握手
    :param proxy:
    :return:
    """
    from socket import socket, AF_INET, SOCK_STREAM
    s = socket(AF_INET, SOCK_STREAM)
    ip, port = proxy.split(':')
    result = s.connect_ex((ip, int(port)))
    return True if result == 0 else False

def validRawProxy(proxy):
    """
    进行第一次代理检验 访问https://www.baidu.com 访问比httpbin.org快
    :param proxy:
    :return:
    """
    if isinstance(proxy, bytes):
        proxy = proxy.decode("utf8")
    proxies = {"http":"http://{proxy}".format(proxy=proxy), "https": "https://{proxy}".format(proxy=proxy)}
    headers = {
        "User-Agent": "Mozilla/5.0 (123456 NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    }
    try:
        r = requests.get('https://httpbin.org', proxies=proxies, headers=headers, timeout=6)
        return True if r.status_code == 200 else True
    except Exception as e:
        pass
    return False

def validUsefulProxy(proxy,myip):
    """
    第二次检验代理是否是高匿IP
    :param myip:
    :param proxy:
    :return:
    """
    if isinstance(proxy, bytes):
        proxy = proxy.decode("utf8")
    headers = {
        "User-Agent": "Mozilla/5.0 (123456 NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    }
    proxies = {"http":"http://{proxy}".format(proxy=proxy), "https": "https://{proxy}".format(proxy=proxy)}
    try:
        # target_url="https://www.zhipin.com/"
        r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=5)
        # r = requests.get(target_url, proxies=proxies, headers=headers, timeout=6)
        if r.status_code == 200:
            j = r.json()
            # 返回的ip字符串 找不到本地ip则为匿名IP即find()返回-1
            return True if j['origin'].find(myip)==-1 else False #第一个高匿  第二个透明 看情况使用
            # return True
    except Exception as e:
        pass
    return False

def validChargeProxy(proxy,myip):
    """
        检验收费代理是否是高匿IP
        :param myip:
        :param proxy:
        :return:
        """
    if isinstance(proxy, bytes):
        proxy = proxy.decode("utf8")
    headers = {
        "User-Agent": "Mozilla/5.0 (123456 NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    }
    proxies = {"http": "http://{proxy}".format(proxy=proxy), "https": "https://{proxy}".format(proxy=proxy)}
    try:
        r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=5)
        # r = requests.get(target_url, proxies=proxies, headers=headers, timeout=6)
        if r.status_code == 200:
            j = r.json()
            # 返回的ip字符串 找不到本地ip则为匿名IP即find()返回-1
            return True if j['origin'].find(myip) == -1 else False  # 第一个高匿  第二个透明 看情况使用
    except Exception as e:
        pass
    return False