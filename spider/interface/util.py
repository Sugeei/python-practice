#!/usr/bin/python
# coding=utf8

from selenium import webdriver
import pandas as pd

df = pd.DataFrame([{'a': 1, 'b': 2
               }])
print(df)
res = [['a',1], ['b',2]]
a = pd.DataFrame(res, columns=['key','value'])
infopd = pd.DataFrame([], columns=['id', 'key','value'])
a['id']='001'
# infopd.append(['001', pd.DataFrame(res)])
# print(infopd)

print(a)
# df = pd.DataFrame(list({'a': 1, 'b': 2}.items()))
from category.listcompanyinfo import infoobj
from config.base import phantomjs

# header =
key = '600125'
url = infoobj.get_src_url(key)
#
driver = webdriver.PhantomJS(executable_path=phantomjs)
driver.get(url)
title = driver.title
page = driver.page_source

# from util..urlhandler import get_soup
from src.headers import header
from src.cookies import cookie

from bs4 import BeautifulSoup
import requests

def get_soup(page):
    # url = params.paramsget('url')
    # header = params.get('header')
    # source = requests.get(url, headers=header)
    soup = BeautifulSoup(page, 'lxml')
    return soup

s = get_soup(page)

# params = {
#     "url": url,
#     "header": header
# }
# t = get_soup(params)
info = infoobj.get_cn_con(s)
a = pd.DataFrame(res, columns=['key','value'])
a['id']=key

# with open()
# pass
