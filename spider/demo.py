#!/usr/bin/python
# -*- coding: UTF-8 -*

#  multiprocess

from util.urlhandler import get_soup
import time

# from mongoconn import mongoset

# table = mongoset('58sale', 'itemurls')

if __name__ == '__main__':
    starttime = time.time()
    print ('start: ')
    print (time.strftime('%Y-%m-%d %H:%M:%S'))

    url = 'https://www.qichacha.com/search?key=91210800MA0QCLUT14'
    # navurls = get_nav_urls(url)
    t = get_soup(url)

    # pool.map(insert_urls_by_nav, navurls)

    endtime = time.time()
    print (time.strftime('%Y-%m-%d %H:%M:%S'))
    elapsed = endtime - starttime