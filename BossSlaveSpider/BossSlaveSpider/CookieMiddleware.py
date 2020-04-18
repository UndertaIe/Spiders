from selenium import webdriver
import requests
from .utils.CookieHandler import getCookie
class CookieMiddleware(object):


    def process_request(self, request, spider):
        request.cookies = getCookie()
        return None
