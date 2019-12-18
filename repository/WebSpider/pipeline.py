#!usr/bin/env python
# #_*_ coding: utf-8 _*_

import time, re
from datetime import datetime

import pymongo
import csv
from xlswriter import excelwriter
from mongoconn import mongoset, mongoinsert,mongoupdate, TPOS

from companylist import companies

pipeline = [
    # {'$match': {'publish_time': {'$gt': '2017-04-02'}}},
    {'$match': {'publish_time': {'$regex': '20'}}},
    # {'$match': {'salary': {'$regex': '\d'}}},
    # {'$match': {'location': {'$in': ['北京', '上海', '广州', '深圳', '杭州']}}},
    # {'$match': {'company_name': {'$in': companies}}},
    # {'$match': {'original_site_name': {'$in': ['猎聘','']}}},
    {'$match': {'degree': {'$regex': "[本硕]"}}},
    {'$match': {'year_experience': {'$regex': "[3-4]{1}"}}},
    {'$match': {'position_name': {'$regex': "[数据]"}}},
    # {'$match': {'position_name': {'$regex': "[数据算法AI机器智能虚拟]"}}},
    # #{'age' : {'$in' : [10, 22, 26]}}
    {'$sort': {'year_experience':1}},#{'age' : {'$in' : [10, 22, 26]}}
    # {'$project': {'_id':0,'publish_time':1, 'position_name':1,}},
    # {'$gt': {'publish_time': '2016-12-01'}},
    # {'$match': {'saletime': ''}},
    # {'$match': {'company': {"$in": regcomp}}},
    # {'$group': {'_id': {'$slice': ['$address', 1, 1]}, 'counts': {'$sum': 1}}}
]
