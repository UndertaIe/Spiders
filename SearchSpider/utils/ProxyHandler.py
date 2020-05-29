import requests
from config import PROXY_URL,PROXY_METHOD

#获取一随机代理
def getProxy():
    url =PROXY_URL+PROXY_METHOD["get"]
    try:
        aproxy = requests.get(url,headers={"User-Agent":"-*-SearchSpider-*-"}).json()
    except:
        print("###[ERROR] ProxyHandler.getProxy RequestException ###")
    return aproxy

#获取一随机收费代理
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
    try:
        proxies = requests.get(url,headers={"User-Agent":"-*-SearchSpider-*-"}).json()
    except:
        print("###[ERROR] ProxyHandler.getAllProxy RequestException ###")
    return proxies

#获取服务器代理数
def getProxyCount():
    url = PROXY_URL+PROXY_METHOD["get_status"]
    try:
        count = requests.get(url,headers={"User-Agent":"-*-SearchSpider-*-"}).json()
    except:
        print("###[ERROR] ProxyHandler.getProxyCount RequestException ###")
    return count

if __name__ == "__main__":
    test_proxy = getProxy()
    assert test_proxy is not None
    test_all_proxy = getAllProxy()
    assert test_all_proxy is not None
    testProxyCount = getProxyCount()
    assert testProxyCount is not None