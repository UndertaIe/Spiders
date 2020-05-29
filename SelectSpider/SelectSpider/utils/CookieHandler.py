
import requests
from requests import RequestException
from ..settings import COOKIE_URL
from ..settings import COOKIE_METHOD

def getCookie():
    url = COOKIE_URL+COOKIE_METHOD['get']
    cookie = None
    try:
        r = requests.get(url=url,timeout=3,headers={"UserAgent":"-*-SelectSpider-*-"})
        if r.status_code==200:
            cookie = r.json()
        r.close()
    except:
        print("###[ERROR] CookieHandler.getCookie RequestException ###")
    return cookie if cookie!= {} and cookie is not None else None
def getCookeCount():
    url = COOKIE_URL + COOKIE_METHOD['count']
    count = None
    try:
        r = requests.get(url=COOKIE_URL,timeout=3,headers={"UserAgent":"-*-SelectSpider-*-"})
        count = int(r.text)
    except:
        print("###[ERROR] CookieHandler.getCookeCount RequestException ###")
    return count



if __name__ == "__main__":
    test_cookie = getCookie()
    assert test_cookie is not None