
import redis
from redis import ConnectionError
from ..settings import REDIS_PARAMS,SEARCH

class RedisHandler:
    def __init__(self, host=None, port=None, pwd=None, search=SEARCH):
        """
        初始化redis操作类
        :param host: redis ip
        :param port: redis port
        :param pwd: redis requirepass
        :param search: 搜索岗位 redis的key值
        """
        try:
            redis_host = host or REDIS_PARAMS['host']
            redis_port = port or REDIS_PARAMS['port']
            redis_pwd = pwd or REDIS_PARAMS['password'] #远程连接密码认证
            self.con = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_pwd)#远程密码认证
            # self.con = redis.StrictRedis(host=redis_host, port=redis_port, db=0) #本地认证
        except:
            print("###[ERROR] RedisHandler.Connection ConnectionError ###")
        self.site = search.split(':')[0]
        self.search = search
        self.encoding = "utf-8"

    # 向工作集合插入一个搜索项 保持插入顺序 先进先出
    def insertSearch(self,jobStr):
        if jobStr is not None and jobStr != "":
            flag = self.con.rpush(self.search, self._encode(jobStr))
        else:
            flag = 0
        return flag

    # 从redis 搜索项列表中 获取一个工作搜索项
    def getSearch(self):
        job = self.con.lpop(self.search)
        return self._decode(job) if job is not None else None

    # 向redis插入Job+City查询后或下一页的URL 需转化为字节串
    def insertSelectURL(self,job,select_url):
        selectKey = "{}:{}:select_urls".format(self.site,job)
        flag = self.con.sadd(selectKey, self._encode(select_url))
        return flag

    # 向redis插入Item对应的细节URL 需转化为字节串
    def insertDetailURL(self,job,detail_url):
        detailKey = "{}:{}:detail_urls".format(self.site,job)
        flag = self.con.sadd(detailKey, self._encode(detail_url))
        return flag

    # 返回当前redis_key的url个数
    def get_current_redis_key_len(self,redis_key):
        flag = self.con.scard(redis_key)
        return flag

    # 在redis中得到所有"Boss:*:select_urls"模式的key，返回一个key让mslave作为redis_key。
    def get_redis_select_key(self):
        keys = self.con.keys("{}:*:select_urls".format(self.site))
        return self._decode(keys[0]) if len(keys)!=0 else None

    # 在redis中得到所有"Boss:*:detail_urls"模式的key，返回一个key让slave作为redis_key。
    def get_redis_detail_key(self):
        keys = self.con.keys("{}:*:detail_urls".format(self.site))
        return self._decode(keys[0]) if len(keys)!=0 else None

    def _encode(self, string):
        encoded = string.encode(self.encoding)
        return encoded

    def _decode(self, byte):
        decoded = byte.decode(self.encoding)
        return decoded

    def close(self):
        try:
            self.con.close()
        except:
            print("### RedisHandler.close RedisCloseException ###")

if __name__ == "__main__":
    pass
