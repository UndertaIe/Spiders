

# cookie获取服务端口
API_SERVER = "127.0.0.1"
API_PORT = 7788

#Cookie最小值，低于此值则从服务器获取Cookie
COOKIE_MIN = 100

COOKIEMAXUSE = 4
POOLSIZE = 2
HEADLESS_NUM = 2  #无头浏览器并发个数
UPDATE_TIME = 60 * 5
EXPIRE_TIME = 60 * 30
DB_CONFIG = {
    #'DB_TYPE': 'mongodb',
    #'DB_CONNECT_STRING':'mongodb://localhost'
    # 'DB_CONNECT_STRING': 'sqlite:///' + os.path.dirname(__file__) + '/data/proxy.db'
    #  DB_CONNECT_STRING : 'mysql+mysqldb://root:root@localhost/proxy?charset=utf8'
    'DB_TYPE': 'redis',
    'DB_STRING': 'redis://localhost:6379/1',
}

#网站URL 通过selenium获取Cookie
COOKIE_URLS = ["https://www.zhipin.com/c101020100/?query=python&ka=sel-city-101020100",\
              "https://www.zhipin.com/c101040100/?query=python&ka=sel-city-101040100",\
              "https://www.zhipin.com/c101040100/?ka=sel-city-101040100",\
              "https://www.zhipin.com/c101020100/?ka=sel-city-101020100",\
              "https://www.zhipin.com/job_detail/?ka=header-job",\
              "https://www.zhipin.com/job_detail/?query=c%2B%2B&city=101020100&industry=&position=",\
              "https://www.zhipin.com/c101280600/?query=c%2B%2B&ka=sel-city-101280600",\
              "https://www.zhipin.com/c101190400/?ka=sel-city-101190400"]