import requests
from config import PROXY_URL,PROXY_METHOD

#获取一随机代理 不稳定速度较慢
def getProxy():
    url =PROXY_URL+PROXY_METHOD["get"]
    aproxy = None
    try:
        r = requests.get(url,headers={"User-Agent":"-*-CookiePool-*-"},timeout=3)
        if r.status_code==200:
            aproxy = r.json()
    except:
        print("###[ERROR] ProxyHandler.getProxy Exception ###")
    return aproxy

#获取一随机收费代理 稳定高速
def getChargeProxy():
    aproxy = None
    url =PROXY_URL+PROXY_METHOD["get_charge"]
    try:
        r = requests.get(url,headers={"User-Agent":"-*-DetailSpider-*-"},timeout=3)
        if r.status_code==200:
            aproxy = r.json()
    except:
        print("###[ERROR] ProxyHandler.getChargeProxy RequestException ###")
    return aproxy

#获取服务器所有代理
def getAllProxy():
    url = PROXY_URL+PROXY_METHOD["get_all"]
    proxies = None
    try:
        r = requests.get(url,headers={"User-Agent":"-*-CookiePool-*-"},timeout=3)
        if r.status_code==200:
            proxies = r.json()
    except:
        print("###[ERROR] ProxyHandler.getAllProxy Exception ###")
    return proxies

#获取服务器代理数
def getProxyCount():
    url = PROXY_URL+PROXY_METHOD["get_status"]
    count = None
    try:
        r = requests.get(url,headers={"User-Agent":"-*-CookiePool-*-"},timeout=3)
        if r.status_code==200:
            count = r.json()
    except:
        print("###[ERROR] ProxyHandler.getProxyCount Exception ###")
    return count

if __name__ == "__main__":
    test_proxy = getProxy()
    print(test_proxy)
    assert test_proxy is not None
    test_all_proxy = getAllProxy()
    assert test_all_proxy is not None
    testProxyCount = getProxyCount()
    assert testProxyCount is not None