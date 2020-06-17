#!/usr/bin/python 
# -*- coding: utf-8 -*-

from selenium import webdriver

from selenium.webdriver.remote.remote_connection import LOGGER
import logging
import platform
from utils.UserAgentHandler import getUserAgent
'''
    获取webdriver.Chrome
'''
def getDriver(driverType='chrome'):
    if driverType=="chrome":
        return getChromeDriver()
    elif driverType=="firefox":
        return getFirefoxDriver()
    elif driverType=="phantomjs":
        return getPhantomjs()
    else:
        return None

def getChromeDriver():
    options = webdriver.ChromeOptions()
    #不使用无头浏览器可使运行速度更快并且无检测风险
    options.add_argument("--headless")  # 设置浏览器为headless无界面模式
    # options.add_argument("--disable-gpu")
    options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片
    options.add_argument('--no-sandbox')  # 非安全模式
    options.add_argument("disable-infobars")
    # options.add_argument('--proxy-server=%s' % proxy) #设置代理
    #必须设置user-agent否则会被防爬虫系统检测 默认headless模式 useragent为 headless chrome
    options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"')
    #不能开启这个 否则会被检测出来爬虫
    #options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('excludeSwitches', ['enable-logging']) #关闭日志命令行输出
    # console不输出log文件
    LOGGER.setLevel(logging.ERROR)

    logging.getLogger('requests').setLevel(logging.ERROR)
    if platform.system()=="Windows":
        # $需要将chromedriver.exe放到path中$
        driver = webdriver.Chrome(options=options, executable_path="chromedriver.exe")
    else:
        driver = webdriver.Chrome(options=options, executable_path="chromedriver")
    #使window.navigator.webdriver值为undefined 从而绕过无头浏览器防爬策略
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
    return driver

'''
    获取webdriver.Firefox
'''
def getFirefoxDriver():
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    profile = webdriver.FirefoxProfile()
    # # 设置代理IP
    # profile.set_preference('network.proxy.http', proxy[0])
    # # 设置代理端口，注意端口是int类型，不是字符串
    # profile.set_preference('network.proxy.http_port', int(proxy[1]))
    # # 设置htpps协议也使用该代理
    # profile.set_preference('network.proxy.ssl', proxy[0])
    # profile.set_preference('network.proxy.ssl_port', proxy[1])
    if platform.system() == "Windows":
        driver = webdriver.Firefox(executable_path="geckodriver.exe",options=options)
    else:
        driver = webdriver.Firefox(executable_path="geckodriver.exe", options=options)

'''
    获取webdriver.Phantomjs
'''
def getPhantomjs():
    cap = webdriver.DesiredCapabilities.PHANTOMJS
    cap["phantomjs.page.settings.resourceTimeout"] = 2000
    cap["phantomjs.page.settings.loadImages"] = False
    cap["phantomjs.page.settings.disk-cache"] = True
    # phantomjs --proxy=ip:port --proxy-type=[http|socks5|none] demo.js
    cap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    if platform.system() == "Windows":
        driver = webdriver.PhantomJS(desired_capabilities=cap,executable_path="phantomjs.exe")
    else:
        driver = webdriver.PhantomJS(desired_capabilities=cap, executable_path="phantomjs")
    return driver

def driverChangeOptions(driver):
    pass



# 可在此处测试driver是否可以正常运行。
if __name__ == "__main__":
    pass