# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mongoengine import *
from django.db import models

'''class BossItem(scrapy.Item):
    # define the fields for your item here like:
    job =  #职位
    company =  #公司
    city =  #城市
    exp =  #工作经验
    requirement =  # 学历
    salary =  #薪资
    welfares =  #福利
    dutys =  #岗位职责
    publish =  #发布时间
    address =  # 详细地址
    url =  #细节链接页面'''
# Create your models here.
class ItemInfo(Document):
    job =  StringField()# 职位
    company = StringField() # 公司
    city = StringField() # 城市
    exp = StringField() # 工作经验
    requirement = StringField() # 学历
    salary = StringField() # 薪资
    welfares = StringField() # 福利
    dutys = StringField() # 岗位职责
    publish = StringField() # 发布时间
    address = StringField() # 详细地址
    url = StringField() # 细节链接页面''
    #指定Collection
    meta = {'abstract':True}

class PythonItemInfo(ItemInfo):
    meta = {'collection':'Python'}
class CppItemInfo(ItemInfo):
    meta = {'collection':'C++'}
class JavaItemInfo(ItemInfo):
    meta = {'collection': 'Java'}
class CItemInfo(ItemInfo):
    meta = {'collection': 'C'}
