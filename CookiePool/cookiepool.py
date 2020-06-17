from multiprocessing import Value, Queue, Process
import sys
import os
from main.DbManager import storeCookie
from main.Generator import startCookiePool
from api.cookieAPI import start_cookie_server
import fire
from config import COOKIE_MIN,HEADERS,API_SERVER,API_PORT,USE_PROXY

def start(count=COOKIE_MIN, proxy=USE_PROXY, ip=API_SERVER, port=API_PORT):
    """生成器与API进程"""
    try:
        print(HEADERS)
        CookieCounter = Value('i', 0) #实时数目
        genCount = Value('i',count) #需要生成的个数
        buffer = Queue()
        Pro1 = Process(target=startCookiePool, args=(buffer, CookieCounter, genCount, proxy))
        # Pro2 = Process(target=startCookiePool, args=(buffer, CookieCounter, genCount, proxy))
        Save = Process(target=storeCookie, args=(buffer, CookieCounter))
        Server = Process(target=start_cookie_server, args=(ip, port))
        Pro1.start()
        Server.start()
        # Pro2.start()
        Save.start()
        Pro1.join()
        # Pro2.join()
        Server.join()
        Save.join()
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        sys.exit(0)

''' cookie生成器 '''
def gen(count=COOKIE_MIN, proxy=USE_PROXY):
    try:
        print(HEADERS)
        CookieCounter = Value('i', 0) #实时数目
        genCount = Value('i',count) #需要生成的个数
        buffer = Queue()
        Pro1 = Process(target=startCookiePool, args=(buffer, CookieCounter, genCount, proxy))
        # Pro2 = Process(target=startCookiePool, args=(buffer, CookieCounter, genCount, proxy))
        Save = Process(target=storeCookie, args=(buffer, CookieCounter))
        Pro1.start()
        # Pro2.start()
        Save.start()
        Pro1.join()
        # Pro2.join()
        Save.join()
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        sys.exit(0)

def api(ip=API_SERVER, port=API_PORT):
    print(HEADERS)
    start_cookie_server(ip=ip, port=port)

if __name__ == "__main__":
    fire.Fire()

