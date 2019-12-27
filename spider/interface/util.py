# coding=utf8
from category.listcompanyinfo import infoobj
# from util..urlhandler import get_soup
from src.headers import header
from src.cookies import cookie

from bs4 import BeautifulSoup
import requests
# coding:utf-8
# 引入selenium中的webdriver
import re
from urllib import urlretrieve
from selenium import webdriver


def get_soup(params):
    url = params.get('url')
    header = params.get('header')
    source = requests.get(url, headers=header)
    soup = BeautifulSoup(source.text, 'lxml')
    return soup


# header =
key = '600125'
url = infoobj.get_src_url(key)
params = {
    "url": url,
    "header": header
}
t = get_soup(params)
infoobj.get_cn_con(t)
pass
