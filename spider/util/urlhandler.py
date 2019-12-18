#!usr/bin/env python
# _*_ coding: utf-8 _*_
#
#  functions to get item urls

from bs4 import BeautifulSoup
import requests
import time

# from mongoconn import mongoset, mongoinsert


def get_soup(url):
    source = requests.get(url)
    soup = BeautifulSoup(source.text, 'lxml')
    return soup


def combineurls(url, page):
    pageurls = []
    for i in range(1, page + 1):
        pageurl = '{}{}/'.format(url, i)
        pageurls.append(pageurl)
    return pageurls


def get_nav_urls(url):
    soup = get_soup(url)
    navlist = soup.select('ul.ym-mainmnu span.dlb > a')
    absurls = []
    for submnu in navlist:
        try:
            absurl = url[0:-11] + submnu.get('href')
        except TypeError:
            pass
        except:
            pass
        if absurl not in absurls:
            absurls.append(absurl)
    return absurls


def get_page_urls(url):
    #  get urls with pages id
    urls = combineurls(url + 'pn', 70)
    return urls


def get_page_urls_bk(url):
    curpage = 1
    maxpage = 0
    while curpage > maxpage:
        maxpage = curpage
        pageurl = url + 'pn' + str(maxpage)
        soup = get_soup(pageurl)
        pager = soup.select('div.pager > a')
        pagenum = pager[len(pager) - 3].select('span')[0].get_text()  #### -3是临时办法， 需要再想想
        curpage = int(pagenum)
    urls = combineurls(url + 'pn', maxpage)
    return urls


def listtodict(urls):
    datamany = []
    for itemurl in urls:
        data = {
            'itemurl': itemurl
        }
        datamany.append(data)
    return datamany


def get_item_urls(url):
    soup = get_soup(url)
    print(url)
    itemlist = soup.select('tr.zzinfo > td.img > a')
    itemurls = []
    if len(itemlist):
        for item in itemlist:
            try:
                itemurl = item.get('href')
            except:
                pass
            itemurls.append(itemurl)
    # time.sleep(1)
    return itemurls


def getemtext(element):
    return element.get_text().strip().replace('\t', '').replace('\n', '').replace(' ', '')


def get_urls_by_nav(navurl):
    navurls = get_page_urls(navurl)
    for pageurl in navurls:
        itemurls = get_item_urls(pageurl)
        print(listtodict(itemurls))
        # mongoinsert(table, listtodict(itemurls))


# table = mongoset('58sale', 'itemurls')
#
#
# def insert_urls_by_nav(navurl):
#     navurls = get_page_urls(navurl)
#     for pageurl in navurls:
#         itemurls = get_item_urls(pageurl)
#         # mongoinsert(table, listtodict(itemurls))
#         if itemurls:
#             table.insert_many(listtodict(itemurls))


if __name__ == '__main__':
    url = 'http://sh.58.com/sale.shtml'
    get_nav_urls(url)
