import sys,os
from config import DB_CONFIG

sys.path.append(os.path.dirname(__file__) + os.sep + '../')
from ..utils import DBExceptions
from ..utils.tran import driver2cookie

try:
    if DB_CONFIG['DB_TYPE'] == 'mongodb':
        from db.MongoHandler import MongoHandler as DbHandler
    elif DB_CONFIG['DB_TYPE'] == 'redis':
        from db.RedisHandler import RedisHanler as DbHandler
    dbHandler = DbHandler()
except Exception as e:
    raise DBExceptions.ConException


#将cookie写入数据库
def storeCookie(buffer,cookieCount):
    goodCount = 0
    badCount = 0
    while True:
        try:
            raw_cookie = buffer.get(timeout=300)
            cookie = driver2cookie(raw_cookie)
            if raw_cookie is not None:
                f = dbHandler.insert(cookie)
                if f == 1:
                    goodCount += 1
                else:
                    badCount += 1
            else:
                badCount += 1
            mes = " | CookiePool | ------>>>>>>>> good Cookie num {},bad Cookie num {},Queue Cookies: {} ".format(goodCount,badCount,buffer.qsize())
            sys.stdout.write(mes + "\r")
            sys.stdout.flush()
        except BaseException:
            if cookieCount.value != 0:
                goodCount += cookieCount.value
                cookieCount.value = 0
                mes = " | CookiePool | ------>>>>>>>> good Cookie num {},bad Cookie num {}".format(goodCount,badCount)
                sys.stdout.write(mes+"\r")
                sys.stdout.flush()
                goodCount = 0
                badCount = 0


