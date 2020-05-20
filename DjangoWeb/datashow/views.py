# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import PythonItemInfo,CItemInfo,CppItemInfo,JavaItemInfo
from django.core .paginator import Paginator
from mongoengine import connect
from mongoengine import disconnect
import re
disconnect()
connect("Cookies", host='127.0.0.1')
# Create your views here.

def document(request):
    limit=20
    pythonItemInfo = PythonItemInfo.objects
    cppItemInfo = CppItemInfo.objects
    javaItemInfo = JavaItemInfo.objects
    cItemInfo = CItemInfo.objects
    itemCount = pythonItemInfo.count() + cppItemInfo.count() + javaItemInfo.count() + cItemInfo.count()

    pageinator=Paginator(pythonItemInfo,limit)
    page=request.GET.get('page',1)
    loaded = pageinator.page(page)
    cities=pythonItemInfo.distinct("city")
    citycount=len(cities)
    context={
        'itemInfo':loaded,
        'counts':itemCount,
        'cities':cities,
        'citycount':citycount
    }
    return render(request,'document.html',context)

def tran(s):
    par = re.compile("\d+")
    try:
        s1,s2 = par.findall(s)
    except:
        return 0
    return (int(s1)+int(s2))/2

'''返回热门城市后端开发薪酬直方图,热门编程语言薪酬直方图'''
def histogram():
    ##直方图
    citys = ['北京', '上海', '广州', '深圳', '杭州', '天津', '西安', '苏州', '武汉', '厦门', '长沙', '成都', '郑州', '重庆']
    citysCmp = [] #各地区薪酬对比直方图数据
    lansCmp = [] #各语言薪酬对比直方图数据
    lansCmpDict = {'salarys':[0,0,0,0], 'count':[0,0,0,0]}#后端开发语言薪酬对比直方图 不同语言的数据库个数

    pythonItemInfo = PythonItemInfo.objects
    cppItemInfo = CppItemInfo.objects
    javaItemInfo = JavaItemInfo.objects
    cItemInfo = CItemInfo.objects

    for city in citys:
        salarys = 0
        city_cmp_count = 0 #一个城市四种开发语言的数据库个数
        for pythonItem in pythonItemInfo(city=city):
            salary1 = tran(pythonItem.salary)
            if salary1 != 0:
                salarys += salary1
                city_cmp_count += 1
                lansCmpDict['salarys'][0] += salary1
                lansCmpDict['count'][0] += 1
        for cppItem in cppItemInfo(city=city):
            salary2 = tran(cppItem.salary)
            if salary2 != 0:
                salarys += salary2
                city_cmp_count += 1
                lansCmpDict['salarys'][1] += salary2
                lansCmpDict['count'][1] += 1
        for javaItem in javaItemInfo(city=city):
            salary3 = tran(javaItem.salary)
            if salary3 != 0:
                salarys += salary3
                city_cmp_count += 1
                lansCmpDict['salarys'][2] += salary3
                lansCmpDict['count'][2] += 1
        for cItem in cItemInfo(city=city):
            salary4 = tran(cItem.salary)
            if salary4 != 0:
                salarys += salary4
                city_cmp_count += 1
                lansCmpDict['salarys'][2] += salary4
                lansCmpDict['count'][2] += 1
        if city_cmp_count != 0:
            citysCmp.append((salarys / city_cmp_count))
        else:
            citysCmp.append(0)

    for i in range(4):
        if lansCmpDict['count'][i] != 0:
            lansCmp.append(lansCmpDict['salarys'][i]/lansCmpDict['count'][i])
        else:
            lansCmp.append(0)
    return citysCmp, lansCmp

def chart(request):
    ##饼状图
    d1,d2 = histogram()
    context ={
        'data1':d1,
        'data2':d2,
    }
    return render(request,'chart.html',context)
