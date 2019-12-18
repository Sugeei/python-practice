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


import random

timedelay = random.randint(3600,7200)

# TODO delay the spider
time.sleep(timedelay)

