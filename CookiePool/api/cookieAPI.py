

import json
import sys
import web
import config
from db.DbManager import dbHandler
from bson import json_util
urls = (
    '/','get',
    '/get','get',
    '/count','count',
    '/select','select'
    '/delete','delete',
)

def start_cookie_server():
    sys.argv.append("{}:{}".format(config.API_SERVER,config.API_PORT))
    server = web.application(urls, globals())
    server.run()


class get(object):
    def GET(self):
        inputs = web.input()
        json_result = dbHandler.get()
        return json_result

class count(object):
    def GET(self):
        inputs = web.input()
        result = dbHandler.count()
        return result

# class select(object):
#     def GET(self):
#         inputs = web.input()
#         lst_result = dbHandler.select()
#         return lst_result

# class delete(object):
#     params = {}
#     def GET(self):
#         inputs = web.input()
#         json_result = dbHandler.delete(inputs)
#         return json_result


if __name__ == '__main__':
    sys.argv.append('127.0.0.1:7788')
    app = web.application(urls, globals())
    app.run()