
import requests
from requests import RequestException
from ..settings import COOKIE_URL
from ..settings import COOKIE_METHOD

def getCookie():
    url = COOKIE_URL+COOKIE_METHOD['get']
    try:
        r = requests.get(url=url,timeout=3)
        cookie = r.json()
    except RequestException as e:
        print("!!!请求 Cookie 失败!!!")
    return cookie
def getCookeCount():
    url = COOKIE_URL + COOKIE_METHOD['count']
    try:
        r = requests.get(url=COOKIE_URL,timeout=3)
        count = int(r.text)
    except RequestException as e:
        print("!!!请求Cookie Count失败!!!")
    return count



if __name__ == "__main__":
    test_cookie = getCookie()
    assert test_cookie is not None