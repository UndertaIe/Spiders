
from config import DB_CONFIG
import pymongo
import queue
from db.DbHandler import DbHanlder
from bson import json_util
from CookiePool.utils.tran import driver2cookie
from config import COOKIEMAXUSE

class MongoHandler(DbHanlder):

    def __init__(self):
        self.client = pymongo.MongoClient(DB_CONFIG['DB_STRING'], connect=False)
        self.db = self.client['CookiePool']
        self.Cookies = self.db['Cookies']
        #缓冲未实现
        self.buffer = queue.Queue()
    # 插入cookie
    def insert(self, cookie):
        if cookie:
            self.Cookies.insert_one(self.driver2mongo(cookie))

    # 返回所有cookie
    def select(self, cookie):
        lst = list(self.Cookies.find_one(projection={"_id":False}))
        return lst

    # 得到随机cookie
    def get(self):
        while True:
            cookie = self.Cookies.find_one(projection={"_id":False})
            if cookie is None:
                print("!!!DB no data!!!")
                break
            ttl = cookie['ttl'] -1
            if cookie['ttl']>0:
                self.Cookies.find_one_and_update(cookie,{'$set':{'ttl':ttl}})
                break
            elif cookie['ttl'] == 0:
                self.Cookies.find_one_and_delete(cookie)
                break
            else:
                self.Cookies.find_one_and_delete(cookie)
        return json_util.dumps(self.mongo2cookie(cookie))

    #返回cookie个数
    def count(self):
        return self.Cookies.estimated_document_count()

    # 去除无效的cookie
    def remove(self,cookie):
        result = self.Cookies.find_one_and_delete(cookie)
        return json_util.dumps(result)
    # def get2web(self):
    #     return json_util.dumps(self.get())
    # def select2web(self):
    #     return json_util.dumps(self.select())
    @staticmethod
    def driver2mongo(cookie_from_webdriver):
        cookie = driver2cookie(cookie_from_webdriver)
        cookie.setdefault('ttl', COOKIEMAXUSE)
        return cookie

    @staticmethod
    def mongo2cookie(cookie_from_db):
        cookie = {}
        for key in cookie_from_db.keys():
            if key != 'ttl':
                cookie.setdefault(key, cookie_from_db[key])
        return cookie
