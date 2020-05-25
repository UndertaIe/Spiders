import requests
from ..settings import PROXY_URL,PROXY_METHOD

#获取一随机代理
def getProxy():
    url =PROXY_URL+PROXY_METHOD["get"]
    try:
        aproxy = requests.get(url,headers={"UserAgent":"-*-DetailSpider-*-"}).json()
    except ConnectionError:
        print("###[ERROR] GetProxy Error ###")
    return aproxy

#获取服务器所有代理
def getAllProxy():
    url = PROXY_URL+PROXY_METHOD["get_all"]
    try:
        proxies = requests.get(url,headers={"UserAgent":"-*-DetailSpider-*-"}).json()
    except ConnectionError:
        print("###[ERROR] GetAllProxy Error ###")
    return proxies

#获取服务器代理数
def getProxyCount():
    url = PROXY_URL+PROXY_METHOD["get_status"]
    try:
        count = requests.get(url,headers={"UserAgent":"-*-DetailSpider-*-"}).json()
    except ConnectionError:
        print("###[ERROR] GetProxy Count Error ###")
    return count

if __name__ == "__main__":
    test_proxy = getProxy()
    assert test_proxy is not None
    test_all_proxy = getAllProxy()
    assert test_all_proxy is not None
    testProxyCount = getProxyCount()
    assert testProxyCount is not None