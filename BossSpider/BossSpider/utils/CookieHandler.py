
import requests
from requests import RequestException
from ..settings import COOKIE_URL


def getCookie():
    try:
        r = requests.get(url=COOKIE_URL,timeout=5)
        cookie = r.json()
    except RequestException as e:
        print("!!!请求Cookie失败!!!")
    return cookie