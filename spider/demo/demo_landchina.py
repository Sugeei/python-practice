# coding=utf8
# console.log('Hello, world!');
# phantom.exit();


# from category.listcompanyinfo import infoobj
# from util..urlhandler import get_soup
from headers import header

from bs4 import BeautifulSoup
import requests


def get_soup(params):
    url = params.get('url')
    header = params.get('header')
    source = requests.get(url, headers=header)
    soup = BeautifulSoup(source.text, 'lxml')
    return soup


url = "https://www.landchina.com/default.aspx?tabid=263&ComName=default"
params = {
    "url": url,
    "header": header
}
t = get_soup(params)

# infoobj.get_cn_con(t)
pass
