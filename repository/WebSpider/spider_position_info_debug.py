#!/usr/bin/python
# -*- coding: UTF-8 -*

#  multiprocess
#  TODO: a spider goes to lieping.com
#  信息分类存储

from multiprocessing import Pool
import time, re, random
import pymongo


from mongoconn import mongoset, mongoinsert,mongoupdate
from urlhandler import get_nav_urls, get_page_urls, get_item_urls, get_wrapper, get_soup

from mongoconn import TURL as urls
from mongoconn import TPOS as tinfo

#
# def insert_urls_by_nav_bk(navurl):
#     pageurls = get_page_urls(navurl, 'o{}/', 90)
#     #print(pageurls)
#     filteritem = 'div.layoutlist > dl > dt > a'
#     for pageurl in pageurls:
#         itemurls = get_item_urls(pageurl, filteritem)
#         if itemurls:
#             mongoinsert(table, listtodict(itemurls))
#             #table.insert_many(listtodict(itemurls))
#         else:
#             break
# #
# # def insert_urls_by_nav(navurl):
# #     itemclass = navurl.split('/')
# #     flag = True
# #     pid = 1
# #     filteritem = 'div.layoutlist > dl > dt > a'
# #     filtervalid = 'ul.pageLink'
# #     while flag:
# #         pageurl = navurl+'o{}'.format(pid)
# #         itemurls = get_item_urls(pageurl, filteritem, filtervalid)
# #         if itemurls:
# #
# #             # mongoinsert(tinfo, listtodict(itemurls))
# #             pid += 1
# #             #table.insert_many(listtodict(itemurls))
# #         else:
# #             flag = False
# #         time.sleep(8)
# #
#
# def insert_urls_statistic(navurl):
#     itemclass = navurl.split('/')[-2]
#     flag = True
#     pid = 1
#     filteritem = 'div.layoutlist > dl > dt > a'
#     filtervalid = 'ul.pageLink'
#     while flag:
#         pageurl = navurl + 'o{}'.format(pid)
#         itemurls = get_item_urls(pageurl, filteritem, filtervalid)
#         if itemurls:
#
#             mongoinsert(tinfo, listtodict(itemurls))
#             pid += 1
#             # table.insert_many(listtodict(itemurls))
#         else:
#             flag = False
#         time.sleep(8)

from DataSelector import dataFactory

if __name__ == '__main__':
    url = 'https://www.liepin.com/job/197987060.shtml'
    factory = dataFactory()
    # pattern = re.compile('www\.(.*)\.com')
    # webflag = pattern.findall(item, 1)
    webflag = re.search(r'www\.(.*)\.com', url).group(1)
    webitem = factory.dataselector(webflag, '', '')
    soup = get_soup(url)
    # soup = get_wrapper(item, 'div.about-position')
    # pattern = re.compile(r'404')
    # TODO 从读到的soup中尝获取目标字段
    try:
        data = webitem.get_formated_data(soup)
    except:
        pass