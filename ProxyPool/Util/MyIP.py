#!/usr/bin/python 
# -*- coding: utf-8 -*-
import requests

def getMyIP():
    url = "http://httpbin.org/ip"
    url2 = "http://icanhazip.com"
    try:
        r =requests.get(url,timeout=10)
        myip = r.json()
        return myip.get('origin')
    except:
        pass