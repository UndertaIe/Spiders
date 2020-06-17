#!/usr/bin/python 
# -*- coding: utf-8 -*-

from os import system,chdir
import fire

def spider(search=""):
    """
    爬取一条搜索项 SearchSpider -> SelectSpider -> DetailSpider
    :param search: 单次爬取
    :return:
    """
    root(List=search, search=search, single=True)

def spiders(List="", Path=""):
    """
    爬取所有搜索项 SearchSpider => SelectSpider => DetailSpider
    :param List: 工作列表导入
    :param Path: 工作文件导入
    :return:
    """
    root(List=List,Path=Path)

def crawl(search=""):
    """
    爬取所有搜索项 SelectSpider -> DetailSpider 省去SearchSpider搜索爬虫
    :param search: 指定优先爬取工作岗位
    :param single: 单次爬取
    :return:
    """
    selectSpider(search=search, single=True)
    detailSpider(search=search, single=True)

def crawls():
    """
    爬取所有搜索项 SelectSpider => DetailSpider 省去SearchSpider搜索爬虫
    :return:
    """
    selectSpider()
    detailSpider()


def root(List="", Path="", hotCity=True, search="", single=False):
    """
    集成了search，select，detail爬虫的系统命令，实现了站点搜索，数据项的解析，页面详情页的解析。并将结果存储到数据库
    :param List:redis搜索项列表初始化
    :param Path:redis搜索项文件初始化
    :param hotCity:热门城市
    :param search:优先搜索项
    :param single:单一爬取 默认为False
    :return:
    """
    searchSpider(List=List, Path=Path, hotCity=hotCity)

    selectSpider(search=search, single=single)

    detailSpider(search=search, single=single)

def searchSpider(List="", Path="", hotCity=True):
    """
    对站点的准确搜索工作
    :param hotCity: 热门城市
    :param List: redis搜索项列表初始化
    :param Path: redis搜索项文件初始化
    :return:
    """
    chdir("./SearchSpider")
    if isinstance(List, tuple):
        List = ",".join(List)

    if isinstance(List,str) and isinstance(Path,str):
        cli = "python searchSpider.py task --List {List} --Path {Path} --hotCity {hotCity}".format(List=List, Path=Path, hotCity=hotCity)
    if isinstance(List,str) and not isinstance(Path,str):
        cli = "python searchSpider.py task --List {List} --hotCity {hotCity}".format(List=List, hotCity=hotCity)
    if not isinstance(List,str) and not isinstance(Path,str):
        cli = "python searchSpider.py task --hotCity {hotCity}".format(hotCity=hotCity)
    if not isinstance(List, str) and isinstance(Path, str):
        cli = "python searchSpider.py task --Path {Path} --hotCity {hotCity}".format(hotCity=hotCity, Path=Path)

    system(cli)
    chdir("..")

def selectSpider(search="", single=False):
    """
    获取*:select_urls模式的url 并将解析后的细节页面url存储到redis的*:detail_urls key值中
    :param search: 优先搜索项 默认为空字符串
    :param single: 单一爬取 默认为False
    :return:
    """

    chdir("./SelectSpider")
    system("scrapy crawl boss -a search={search} -a single={single}".format(search=search, single=single))
    chdir("..")

def detailSpider(search="", single=False):
    """
    获取*:select_urls模式的url 并将工作详情页面存储到mongodb中
    :param search: 优先搜索项 默认为空字符串
    :param single: 单一爬取 默认为False
    :return:
    """

    chdir("./DetailSpider")
    system("scrapy crawl boss -a search={search} -a single={single}".format(search=search, single=single))
    chdir("..")

def proxypool(command):
    """
    代理池
    :param command: api or schedule
    :return:
    """
    chdir("ProxyPool/cli")
    if command == "schedule":
        system("python proxypool.py schedule")
    elif command == "api":
        system("python proxypool.py api")
    chdir("../..")

def cookiepool(command, proxy=False, ip="0.0.0.0", port=7700):
    """
    cookie池
    :param command: start or gen or api
    :param proxy: 是否使用代理
    :param ip: api ip
    :param port: api port
    :return:
    """
    chdir("./CookiePool")
    if command == "start":
        system("python cookiepool.py start --proxy {proxy} --ip {ip} --port {port}".format(proxy=proxy,ip=ip,port=port))
    elif command == "gen":
        system("python cookiepool.py gen --proxy {proxy}".format(proxy=proxy))
    elif command == "api":
        system("python cookiepool.py api --ip {ip} --port {port}".format(ip=ip,port=port))
    chdir("..")

if __name__ == "__main__":
    fire.Fire()