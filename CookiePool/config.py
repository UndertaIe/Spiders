#CookiePool生成器配置文件


#===========================
# cookie获取服务API
API_SERVER = "101.200.79.28"
API_PORT = 7788
#===========================

#===========================
#Splash JS渲染引擎接口用于生成Cookie
SPLASH_HOST = "192.168.0.201"
SPLASH_PORT = 8050
SplashUrl = "http://{}:{}/execute".format(SPLASH_HOST,SPLASH_PORT)
#===========================

#===========================
#配置代理服务
PROXY_URL = "http://101.200.79.28:5010/"
PROXY_METHOD = {"get":"get","get_all":"get_all","get_status":"get_status"}
PROXY_EXPIRE = 1 * 30
#===========================


#Cookie最小值，低于此值则从服务器获取Cookie
COOKIE_MIN = 2000

COOKIEMAXUSE = 4   #4
POOLSIZE = 8
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

User_Agent = [ \
        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31', \
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17', \
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17', \
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)', \
        'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)', \
        'Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)', \
        'Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1', \
        'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1', \
        'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:15.0) Gecko/20120910144328 Firefox/15.0.2', \
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201', \
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a3pre) Gecko/20070330', \
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.13; ) Gecko/20101203', \
        'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
        'Opera/9.80 (X11; Linux x86_64; U; fr) Presto/2.9.168 Version/11.50', \
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; de) Presto/2.9.168 Version/11.52', \
        'Mozilla/5.0 (Windows; U; Wsin 9x 4.90; SG; rv:1.9.2.4) Gecko/20101104 Netscape/9.1.0285', \
        'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8.1.7pre) Gecko/20070815 Firefox/2.0.0.6 Navigator/9.0b3', \
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6']

HEADERS = '''
        +------------------+
        |    CookiePool    |
        +------------------+
    '''