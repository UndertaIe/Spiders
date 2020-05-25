from multiprocessing import Value, Queue, Process
import sys
import os
from main.DbManager import storeCookie
from main.Generator import startCookiePool
from api.cookieAPI import start_cookie_server
import fire
from config import COOKIE_MIN,HEADERS

''' cookie生成器 '''
def gen(count=COOKIE_MIN):
    try:
        print(HEADERS)
        CookieCounter = Value('i', 0) #实时数目
        genCount = Value('i',count) #需要生成的个数
        buffer = Queue()
        Pro1 = Process(target=startCookiePool, args=(buffer, CookieCounter,genCount))
        Pro2 = Process(target=startCookiePool, args=(buffer, CookieCounter, genCount))
        Save = Process(target=storeCookie, args=(buffer, CookieCounter))
        Pro1.start()
        Pro2.start()
        Save.start()
        Pro1.join()
        Pro2.join()
        Save.join()
    except KeyboardInterrupt:
        sys.exit(0)

def api(ip="127.0.0.1",port=7788):
    start_cookie_server(ip=ip,port=port)

if __name__ == "__main__":
    fire.Fire()

