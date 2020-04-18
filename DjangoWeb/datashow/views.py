# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import ItemInfo
from django.core .paginator import Paginator
from mongoengine import connect
from mongoengine import disconnect
disconnect()
connect("Cookies", host='127.0.0.1')
# Create your views here.
def document(request):
    limit=15
    bossInfo=ItemInfo.objects
    pageinator=Paginator(bossInfo,limit)
    page=request.GET.get('page',1)
    loaded = pageinator.page(page)
    cities=bossInfo.distinct("city")
    citycount=len(cities)
    context={
        'itemInfo':loaded,
        'counts':bossInfo.count,
        'cities':cities,
        'citycount':citycount
    }
    return render(request,'document.html',context)
def binzhuantu():
    ##饼状图
    citys = []
    bossInfo = ItemInfo.objects
    sums = float(bossInfo.count())
    cities = bossInfo.distinct("city")
    for city in cities:
        length = float(len(bossInfo(city=city)))
        ocu = round(float(length / sums * 100))
        item = [city.encode('raw_unicode_escape'), ocu]
        citys.append(item)
    return citys

def chart(request):
    ##饼状图
    citys=binzhuantu()
    context ={
        # 'count': counts,
        # 'citys': cc,
        'cities':citys,
    }
    return render(request,'chart.html',context)
def cloud(request):
    bossInfo = ItemInfo.objects
    res = bossInfo.distinct('community')
    length=len(res)
    context={
        'count':length,
        'wenzi':res
    }
    return render(request, 'test.html',context)

def test(request):
    bossInfo = ItemInfo.objects
    rr=[]
    res = bossInfo.distinct('community')
    i=0
    while i<500:
        item=res[i]
        rr.append(item)
        i=i+1
    length = len(res)
    context = {
        'count': length,
        'wenzi':  rr
    }
    return render(request,'test.html',context)