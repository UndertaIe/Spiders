import requests
from config import PROXY_URL,PROXY_METHOD

#获取一随机代理
def getProxy():
    url =PROXY_URL+PROXY_METHOD["get"]
    aproxy = None
    try:
        r = requests.get(url,headers={"User-Agent":"-*-CookiePool-*-"},timeout=3)
        if r.status_code==200:
            aproxy = r.json()
    except ConnectionError:
        print("###[ERROR] ProxyHandler.getProxy Error ###")
    return aproxy
#获取服务器所有代理
def getAllProxy():
    url = PROXY_URL+PROXY_METHOD["get_all"]
    proxies = None
    try:
        r = requests.get(url,headers={"User-Agent":"-*-CookiePool-*-"},timeout=3)
        if r.status_code==200:
            proxies = r.json()
    except ConnectionError:
        print("###[ERROR] ProxyHandler.getAllProxy Error ###")
    return proxies

#获取服务器代理数
def getProxyCount():
    url = PROXY_URL+PROXY_METHOD["get_status"]
    count = None
    try:
        r = requests.get(url,headers={"User-Agent":"-*-CookiePool-*-"},timeout=3)
        if r.status_code==200:
            count = r.json()
    except ConnectionError:
        print("###[ERROR] ProxyHandler.getProxyCount Error ###")
    return count

if __name__ == "__main__":
    test_proxy = getProxy()
    print(test_proxy)
    assert test_proxy is not None
    test_all_proxy = getAllProxy()
    assert test_all_proxy is not None
    testProxyCount = getProxyCount()
    assert testProxyCount is not None