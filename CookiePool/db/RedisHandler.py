from redis import Redis

import config
from db.DbHandler import DbHanlder
import redis
import json
from redis.exceptions import RedisError

#zcard(jihe) 个数
#zadd(jihe,{data:score})
#redis.zrevrangebyscore(self.get_index_name("score"), '+inf', '-inf', start=0, num=count)) 得到值

#r.zrevrangebyscore('Coo','+inf','-inf',start=0,num=1)得到一个值
class RedisHanler(DbHanlder):
    def __init__(self, url=None):
        self.redis_url = url or config.DB_CONFIG['DB_STRING']
        self.redis = redis.from_url(self.redis_url)
        self.key = "Cookies"
        self.redis.expire(self.key,config.EXPIRE_TIME)  #设置过期时间
    #插入cookie
    def insert(self,cookie):
        if len(cookie) == 4:
            return 0
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
                print("No data")
                return None
            else:
                cookie = result[0] #此时返回的是字节串
                score = self.redis.zscore(self.key,cookie)
                if score<4: #score<4表示此cookie再次使用
                    self.redis.zadd(self.key, {cookie:(score+1)})
                elif score == 4:#不能再次使用并且移除
                    self.redis.zrem(self.key,cookie)
                else:#不能再次使用且本次也不能使用并且移除
                    self.redis.zrem(self.key, cookie)
                    cookie = None
            if cookie is not None:
                break
            else:
                continue
        return cookie

    def count(self):
        try:
            count = self.redis.zcard(self.key)
        except RedisError:
            print("!!!redis cookie count error!!!")
        return count

    #去除cookie
    def remove(self):
        pass
