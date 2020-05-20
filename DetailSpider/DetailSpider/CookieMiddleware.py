from selenium import webdriver
import requests
from .utils.CookieHandler import getCookie
from time import sleep

class CookieMiddleware(object):


    def process_request(self, request, spider):
        cookie = getCookie()
        if cookie is not None:
            request.cookies = getCookie()
        else:
            print("###[WARNING] Spider request didn't carry Cookie,request may return error page ###")
            sleep(3)
