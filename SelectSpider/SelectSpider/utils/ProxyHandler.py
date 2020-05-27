import requests
from ..settings import PROXY_URL,PROXY_METHOD

#获取一随机代理
def getProxy():
    url =PROXY_URL+PROXY_METHOD["get"]
    aproxy = None
    try:
        r = requests.get(url,headers={"UserAgent":"-*-SelectSpider-*-"},timeout=3)
        if r.status_code==200:
            aproxy = r.json()
    except ConnectionError:
        print("###[ERROR] ProxyHandler.getProxy ConnectionError ###")
    return aproxy

#获取服务器所有代理
def getAllProxy():
    url = PROXY_URL+PROXY_METHOD["get_all"]
    proxies = None
    try:
        r = requests.get(url,headers={"UserAgent":"-*-SelectSpider-*-"},timeout=3)
        if r.status_code==200:
            proxies = r.json()
    except ConnectionError:
        print("###[ERROR] ProxyHandler.getAllProxy ConnectionError ###")
    return proxies

#获取服务器代理数
def getProxyCount():
    count = None
    url = PROXY_URL+PROXY_METHOD["get_status"]
    try:
        r = requests.get(url,headers={"UserAgent":"-*-SelectSpider-*-"},timeout=3)
        if r.status_code == 200:
            count = r.json()
    except ConnectionError:
        print("###[ERROR] ProxyHandler.getProxyCount ConnectionError ###")
    return count

if __name__ == "__main__":
    test_proxy = getProxy()
    assert test_proxy is not None
    test_all_proxy = getAllProxy()
    assert test_all_proxy is not None
    testProxyCount = getProxyCount()
    assert testProxyCount is not None