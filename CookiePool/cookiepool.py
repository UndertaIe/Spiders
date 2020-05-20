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
        print()
        CookieCounter = Value('i', 0) #实时数目
        genCount = Value('i',count) #需要生成的个数
        buffer = Queue()
        Pro = Process(target=startCookiePool, args=(buffer, CookieCounter,genCount))
        save = Process(target=storeCookie, args=(buffer, CookieCounter))
        Pro.start()
        save.start()
        Pro.join()
        save.join()
    except:
        sys.exit(0)

def api(ip="127.0.0.1",port=7788):
    start_cookie_server(ip=ip,port=port)

if __name__ == "__main__":
    fire.Fire()

