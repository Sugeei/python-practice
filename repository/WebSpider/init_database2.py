#!/usr/bin/python
# -*- coding: UTF-8 -*

#  TODO: init database, create table will unique limit

from multiprocessing import Pool
import time, re, random
import pymongo

from mongoconn import mongoset


new = mongoset('openpositiondb', 'positions')
new.create_index([('URL', pymongo.DESCENDING)], unique=True)

table = mongoset('openpositiondb', 'urllist')
table.create_index([('itemurl', pymongo.DESCENDING)], unique=True)
