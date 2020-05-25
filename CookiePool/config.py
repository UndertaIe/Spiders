#CookiePool生成器配置文件


#===========================
# CookiePool提供服务API
API_SERVER = "0.0.0.0"
API_PORT = 7788
#===========================

#===========================
#Splash JS渲染引擎接口用于生成Cookie
#负载均衡nginx ip
SPLASH_HOST = "192.168.0.210"
SPLASH_PORT = 8050
SplashUrl = "http://{}:{}/execute".format(SPLASH_HOST,SPLASH_PORT)
SplashAuthUser="admin"
SplashAuthPwd="nimda0"
#===========================

#===========================
#配置代理服务
PROXY_URL = "http://101.200.79.28:5010/"
PROXY_METHOD = {"get":"get","get_all":"get_all","get_status":"get_status"}
PROXY_EXPIRE = 1 * 30
#===========================


#Cookie最小值，低于此值则从服务器获取Cookie
COOKIE_MIN = 3000

COOKIEMAXUSE = 5   # 4 => 5
POOLSIZE = 4
UPDATE_TIME = 60 * 2
EXPIRE_TIME = 60 * 60 * 24


DB_TYPE = 'redis'   # |
# DB_TYPE = 'mongodb'

MONGODB_HOST="101.200.79.28"
MONGODB_PORT=27016
MONGODB_USER="root"
MONGODB_PWD="mymongodb0"
MONGODB_PARAMS={
    'url':"mongodb://{user}:{pwd}@{host}:{port}/".format(user=MONGODB_USER,pwd=MONGODB_PWD,host=MONGODB_HOST,port=MONGODB_PORT)
}
REDIS_PARAMS = {
    'host':'101.200.79.28',
    'port':6378,
    'password':'myredis0',
    'db':1,
}

#网站URL 通过selenium获取Cookie
COOKIE_URLS = ["https://www.zhipin.com/c101020100/?query=python&ka=sel-city-101020100",\
               "https://www.zhipin.com/c101040100/?ka=sel-city-101040100",\
               "https://www.zhipin.com/c101020100/?ka=sel-city-101020100",\
               "https://www.zhipin.com/job_detail/?ka=header-job",\
               "https://www.zhipin.com/job_detail/?query=c%2B%2B&city=101020100&industry=&position=",\
               "https://www.zhipin.com/c101280600/?query=c%2B%2B&ka=sel-city-101280600",\
               "https://www.zhipin.com/c101190400/?ka=sel-city-101190400",\
               "https://www.zhipin.com/c100010000-p100102/?ka=search_100102",\
               "https://www.zhipin.com/c101180100-p100101/?ka=sel-city-101180100",\
               "https://www.zhipin.com/c101280100-p100101/?ka=sel-city-101280100",\
               "https://www.zhipin.com/c101280600-p100101/?ka=sel-city-101280600",\
               "https://www.zhipin.com/c101190400-p100101/?ka=sel-city-101190400",\
               "https://www.zhipin.com/c101020100-p100101/?ka=sel-city-101020100",\
               "https://www.zhipin.com/c101040100-p100101/?ka=sel-city-101040100",\
               "https://www.zhipin.com/c101110100-p100101/?ka=sel-city-101110100",\
               "https://www.zhipin.com/c101030100-p100101/?ka=sel-city-101030100",\
               "https://www.zhipin.com/c101270100-p100101/?ka=sel-city-101270100",\
               "https://www.zhipin.com/c101230200-p100101/?ka=sel-city-101230200",\
               "https://www.zhipin.com/job_detail/?query=java&city=101121300&industry=&position=",\
               "https://www.zhipin.com/c101190400/?query=java&ka=sel-city-101190400",\
               "https://www.zhipin.com/job_detail/?query=python&city=101020100&industry=&position=",]


HEADERS = '''
        +------------------+
        |    CookiePool    |
        +------------------+
    '''