import requests
from ..settings import PROXY_URL,PROXY_METHOD

#获取一条随机代理
def getProxy():
    url =PROXY_URL+PROXY_METHOD["get"]
    try:
        aproxy = requests.get(url).json()
    except ConnectionError:
        print("!!!GetProxy Error")
    return aproxy
#获取服务器所有代理
def getAllProxy():
    url = PROXY_URL+PROXY_METHOD["get_all"]
    try:
        proxies = requests.get(url).json()
    except ConnectionError:
        print("!!!GetAllProxy Error")
    return proxies

#获取服务器代理数
def getProxyCount():
    url = PROXY_URL+PROXY_METHOD["get_status"]
    try:
        count = requests.get(url).json()
    except ConnectionError:
        print("!!!GetProxyCount Error")
    return count
