

import redis
from redis import ConnectionError
from ..settings import REDIS_IP,REDIS_PORT,RESARCH_NAME

class RedisHandler:
    def __init__(self):
        try:
            self.con = redis.Redis(host=REDIS_IP, port=REDIS_PORT, db=0)
        except ConnectionError:
            print("!!!Redis Connection Error!!!")
        self.selectKey = "Boss:{}:select_urls".format(RESARCH_NAME)
        self.detailKey = "Boss:{}:detail_urls".format(RESARCH_NAME)
        self.encoding = "utf-8"
    #向redis插入Job+City查询后或下一页的URL 需转化为字节串
    def insertSelectURL(self,select_url):
        self.con.sadd(self.selectKey,self._encodeUrl(select_url))
    #向redis插入Item对应的细节URL 需转化为字节串
    def insertDetailURL(self,detail_url):
        self.con.sadd(self.detailKey,self._encodeUrl(detail_url))

    def _encodeUrl(self,url):
        encoded_url = url.encode(self.encoding)
        return encoded_url