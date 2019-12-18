#!usr/bin/env python
#_*_ coding: utf-8 _*_
#
#  connect mongodb

import pymongo
from database import DB


def mongoset(db, table):
    client = pymongo.MongoClient('localhost', 27017)
    data = client[db]
    sheet = data[table]
    return sheet

def mongoinsert(table, data):
    table.insert_many(data)
    try:
        table.insert_many(data)
    except:
        pass

def getmongosize(table):
    return table.find().count()

def mongoupdate(table, key, value):
    table.update(key, value)
    try:
        table.update(key, value)
    except:
        pass

# DB = 'openpositiondb'

TURL = mongoset(DB, 'urllist')
TURL.create_index([('_id', pymongo.DESCENDING)], unique=True)
TURL.create_index([('itemurl', pymongo.DESCENDING)], unique=True)

TPOS = mongoset(DB, 'positions')

from datetime import datetime
c = datetime.today()
print(c.strftime('%Y%m%d'))