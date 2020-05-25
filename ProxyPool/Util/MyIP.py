#!/usr/bin/python 
# -*- coding: utf-8 -*-
import requests

def getMyIP():
    url = "http://httpbin.org/ip"
    url2 = "http://icanhazip.com"
    r =requests.get(url,timeout=5)
    myip = r.json()
    return myip.get('origin')
