#!/usr/bin/python 
# -*- coding: utf-8 -*-

import json
import requests

def getHotCity():
    try:
        from config import hotCitys
    except:
        print("###[WARNING] 配置文件config未定义hotcity ###")
    return hotCitys

def getAllCity():
    try:
        f = open("citys.json", 'r', encoding='utf-8')
        cityJson = json.loads(f.read())
    except:
        print("###[WARNING] 文件读取城市失败 ###")
    return cityJson

def getAllCityFromRequest():
    cityUrl = "https://www.zhipin.com/wapi/zpCommon/data/city.json"
    response = requests.get(cityUrl)
    json_text = json.loads(response.text)['zpData']['cityList']
    # 将json文件转化为字典dic 结构为 dic = {province0:[city0,city1,city2],province1:[city0,city1,city2]...}
    provs = {}
    for i in range(len(json_text)):
        # 获取省份名
        province = json_text[i]['name']
        # 获取所在省份 城市列表
        provinces = json_text[i]['subLevelModelList']
        provs.setdefault(province, [])
        citys = []
        # 分类直辖市和地级市，并归类到字典的值
        if provinces.__len__() > 1:
            for ii in range(len(provinces)):
                citys.append(provinces[ii]['name'])
        else:
            citys.append(province)
        provs[province] = citys
    return provs

