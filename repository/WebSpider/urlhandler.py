#!usr/bin/env python
#_*_ coding: utf-8 _*_
#
#  functions to get item urls

from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import time
import re, random

from mongoconn import mongoset, mongoinsert
from user_agent import ua

def get_soup(url):
    idx = random.randint(0, len(ua)-1)
    proxies = {'http': "207.62.234.53:8118"}

    headers = {
        'User-Agent': ua[idx]
        # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
    source = requests.get(url, proxies=proxies, headers=headers)
    source = requests.get(url, headers=headers)
    # source = requests.get(url)
    soup = BeautifulSoup(source.text, 'lxml')
    return soup

def combineurls(url, page):
    pageurls = []
    for i in range(1, page+1):
        pageurl = url.format(i)
        pageurls.append(pageurl)
    return pageurls

def get_nav_urls(url, urlbase, filter):
    soup = get_soup(url)
    navlist = soup.select(filter)
    absurls = []
    for submnu in navlist:
        try:
            absurl = urlbase + submnu.get('href')
        except TypeError:
            pass
        except:
            pass
        if absurl not in absurls:
            absurls.append(absurl)
    return absurls

def get_page_urls(urlbase, suburl, pagenum=10):
    #  get urls with pages id
    pageurls = []
    for i in range(0, pagenum + 1):
        pageurl = (urlbase + suburl).format(i)
        pageurls.append(pageurl)
    return pageurls

def get_page_urls_bk(url):
    curpage = 1
    maxpage=0
    while curpage > maxpage:
        maxpage = curpage
        pageurl = url + 'pn' + str(maxpage)
        soup = get_soup(pageurl)
        pager = soup.select('div.pager > a')
        pagenum = pager[len(pager)-3].select('span')[0].get_text() #### -3是临时办法， 需要再想想
        curpage = int(pagenum)
    urls = combineurls(url+'pn', maxpage)
    #time.sleep(1)
    return urls

def listtodict(urls):
    datamany = []
    for itemurl in urls:
        data = {
            'itemurl': itemurl,
            'flag': False,      # False means the position of this postion has not been insert into "info" table
        }
        datamany.append(data)
    return datamany

def get_item_urls_bk(url, filter):
    soup = get_soup(url)
    print(url)
    itemlist = soup.select(filter)
    itemurls = []
    if len(itemlist):
        for item in itemlist:
            try:
                itemurl = item.get('href')
            except:
                pass
            itemurls.append(itemurl)
    #time.sleep(1)
    return itemurls

# TODO by giving the url of postion list page, extrat urls of all the positions on this page
# parameter urls is a list.
def get_item_urls(urls, filter, filtervalid=''):

    itemurls = []
    for url in urls:
        sleeptime = random.randint(5, 15)
        soup = get_soup(url)
        # print('start search ' + url)
        if len(soup.select(filtervalid)):
            itemlist = soup.select(filter)
            if len(itemlist):
                for item in itemlist:
                    try:
                        itemurl = item.get('href')
                    except:
                        pass
                    itemurls.append(itemurl)
        # print('sleep ' + str(sleeptime) + 's')
        time.sleep(sleeptime)
    print('[Note]totally ' + str(len(itemurls)) + ' positions found' )
    return itemurls

def getemtext(element):
    return element.get_text().strip().replace('\t', '').replace('\n', '').replace(' ','')

def get_urls_by_nav(navurl):
    navurls = get_page_urls(navurl)
    for pageurl in navurls:
        itemurls = get_item_urls(pageurl)
    return itemurls

def get_wrapper(url, filter):
    soup = get_soup(url)
    # url_data = requests.get(url)

    # soup = BeautifulSoup(url_data.text, "lxml")
    msg = ''
    try:
        msg = soup.select(filter)[0]
    except:
        print(soup)
    return msg

# To be deprecated
# def get_target_info(soup, filter):
#     # soup = get_soup(url)
#     if not soup:
#         return 'soup is empty'
#
#     position = getemtext(soup.select(filter['position'])[0])
#     print(position)
#     pattern = re.compile(u'数据')
#     p2 = re.compile(u'分析')
#     p3 = re.compile(u'机器学习')
#     if not pattern.findall(position) and not p2.findall(position) and not p3.findall(position):
#         return ''
#
#     info = {}
#     keys = ['company',
#                 'firm_type',
#                 'firm_detail',
#                 'position',
#                 'publish_time',
#                 'recruit_type',
#                 'location',
#                 'package',
#                 'job_decri',
#                 'qualification',
#                 'contact_info',
#                 'original_web',
#                 'URL']
#
#     for fi in keys:
#         info[fi] = ''
#         if filter[fi]:
#             try:
#                 info[fi] = getemtext(soup.select(filter[fi])[0])
#             except:
#                 print(soup.select(filter[fi]))
#     try:
#         info['firm_detail'] = getemtext(soup.select(filter['qualification'])[2])
#     except:
#         pass
#     try:
#         pub_t = getemtext(soup.select('div.job-title-left p.basic-infor span')[1])
#         print(pub_t)
#         timenow = datetime.now()
#         if re.match('\d*-\d*-\d', pub_t):
#             info['publish_time'] = pub_t
#         # formattime = pub_t
#         else :
#             formattime = timenow
#             # pt = re.compile(u'刚刚')
#             # if pt.findall(pub_t): formattime = timenow
#             pt = re.compile(u'小时前')
#             if pt.findall(pub_t):
#                 hrs = re.search('\d*', pub_t)
#                 formattime = timenow - timedelta(hours=int(hrs.group(0)))
#             pt = re.compile(u'昨天')
#             if pt.findall(pub_t): formattime = timenow - timedelta(days=1)
#             pt = re.compile(u'前天')
#             if pt.findall(pub_t):
#                 formattime = timenow - timedelta(days=2)
#             info['publish_time'] = formattime.strftime('%Y-%m-%d')
#     except:
#         pass
#
#     return info
#     #print data['image']#title[0].get_text()
#     #downimg(data['image'])

if __name__ == '__main__':

    url = 'http://sh.58.com/sale.shtml'
    get_nav_urls(url)
