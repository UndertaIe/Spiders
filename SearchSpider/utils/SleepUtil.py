#!/usr/bin/python 
# -*- coding: utf-8 -*-
from time import sleep
from random import random



def sleepRandom(i=0):
    sleep(i+random())

def sleepClick():
    """点击事件休眠"""
    sleepRandom(2)

def sleepGet():
    """driver.get事件休眠"""
    sleepRandom(2)

def sleepClear():
    """清除搜索框休眠"""
    sleepRandom()

def sleepInput():
    """搜索框输入休眠"""
    sleepRandom()

def sleepError():
    """发生错误时休眠"""
    sleepRandom(3)

def sleepWarn():
    """发声警告时休眠"""
    sleepRandom(2)


