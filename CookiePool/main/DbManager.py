
import sys,os
from config import DB_TYPE

try:
    if DB_TYPE == 'mongodb':
        from db.MongoHandler import MongoHandler as DbHandler
    elif DB_TYPE == 'redis':
        from db.RedisHandler import RedisHanler as DbHandler
    dbHandler = DbHandler()
except Exception as e:
    raise ConnectionError


#将cookie写入数据库
def storeCookie(buffer,cookieCount):
    goodCount = 0
    badCount = 0
    while True:
        try:
            cookieCount.value = dbHandler.count() # 将redis数据库中cookie数目赋给cookieCount
            cookie = buffer.get(timeout=1024)
            if cookie is not None and len(cookie) == 1:
                f = dbHandler.insert(cookie)
                if f == 1:
                    goodCount += 1
                else:
                    badCount += 1
            else:
                badCount += 1
            mes = " | CookiePool | ------>>>>>>>> good Cookie num {},bad Cookie num {},Redis Cookies: {} \r".format(goodCount,badCount,cookieCount.value)
            sys.stdout.write(mes)
            sys.stdout.flush()
        except BaseException: #超时异常
            if cookieCount.value != 0:
                goodCount += cookieCount.value
                cookieCount.value = 0
                mes = " | CookiePool | ------>>>>>>>> good Cookie num {},bad Cookie num {},Redis Cookies: {} \r".format(goodCount,badCount,cookieCount.value)
                sys.stdout.write(mes)
                sys.stdout.flush()
                goodCount = 0
                badCount = 0


