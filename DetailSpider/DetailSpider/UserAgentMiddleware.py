
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
#from fake_useragent import UserAgent
from utils.UserAgentHandler import getUserAgent

class RotateUserAgentMiddleware(UserAgentMiddleware):
    """
        a useragent middleware which rotate the user agent when crawl websites

        if you set the USER_AGENT_LIST in settings,the rotate with it,if not,then use the default user_agent_list attribute instead.
    """

    # the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    # for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
    def __init__(self, user_agent=''):
        pass

    def process_request(self, request, spider):
        ua = getUserAgent()
        request.headers.setdefault('User-Agent', ua)