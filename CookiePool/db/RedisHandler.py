from redis import Redis


import redis
import json
from redis.exceptions import RedisError
from db.DbHandler import DbHanlder
from config import REDIS_PARAMS,COOKIEMAXUSE
import config
#zcard(jihe) 个数
#zadd(jihe,{data:score})
#redis.zrevrangebyscore(self.get_index_name("score"), '+inf', '-inf', start=0, num=count)) 得到值

#r.zrevrangebyscore('Coo','+inf','-inf',start=0,num=1)得到一个值
class RedisHanler(DbHanlder):
    def __init__(self, host=None, port=None, pwd=None):
        redis_host = host or REDIS_PARAMS['host']
        redis_port = port or REDIS_PARAMS['port']
        redis_pwd = pwd or REDIS_PARAMS['password']
        redis_db = pwd or REDIS_PARAMS['db']
        self.redis = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_pwd, db=redis_db)
        self.key = "Cookies"
        self.redis.expire(self.key,config.EXPIRE_TIME)  #设置过期时间
        self.reuse = COOKIEMAXUSE
    #插入cookie
    def insert(self,cookie):
        try:
            result = self.redis.zadd(self.key,{json.dumps(cookie):1})
        except RedisError:
            print("!!!redis cookie insert error!!!")
        return result
    #返回所有cookie
    def select(self,cookie):
        try:
            cookies = self.redis.zrevrangebyscore(self.key, '+inf', '-inf', start=0,num=500)
        except RedisError:
            print("!!!redis cookie select error!!!")
        if cookies is not None:
            return cookies
        else:
            print("No data")
            return None
    #得到随机cookie
    def get(self):
        while True:
            try:
                result = self.redis.zrevrangebyscore(self.key,'+inf','-inf',start=0,num=1)
            except RedisError:
                print("!!!redis cookie get error!!!")
                break
            if result is None:
                return {}
            try:
                cookie = result[0] #此时返回的是字节串数组
                score = self.redis.zscore(self.key,cookie)
                if score<self.reuse: #score < reuse表示此cookie再次使用
                    self.redis.zadd(self.key, {cookie:(score+1)})
                elif score == self.reuse:#不能再次使用并且移除
                    self.redis.zrem(self.key,cookie)
                else:#不能再次使用且本次也不能使用并且移除
                    self.redis.zrem(self.key, cookie)
                    cookie = None
            except:
                return None
            if cookie is not None:
                break
        return cookie

    def count(self):
        cookie_count = None
        try:
            cookie_count = self.redis.zcard(self.key)
        except RedisError:
            print("!!!redis cookie count error!!!")
        return cookie_count if cookie_count is not None else 0

    #去除cookie
    def remove(self):
        pass
