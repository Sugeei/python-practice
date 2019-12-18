#!usr/bin/env python
# #_*_ coding: utf-8 _*_

import time, re
from datetime import datetime

import pymongo
import csv
from xlswriter import excelwriter
from mongoconn import mongoset, mongoinsert,mongoupdate, TPOS

from companylist import companies

column = 'position_name,position_type,department,location,isfulltime,year_experience,degree,salary,majorwanted,numberofrecuit,attractive,job_description,company_name,industry,company_type,company_level,company_size,company_url,publish_time,original_site_name,position_url'
headers = '''职位名称
            ,职位分类标签
            ,部门
            ,工作地点
            ,工作性质
            ,经验
            ,学历
            ,薪资
            ,专业要求
            ,招聘人数
            ,职位诱惑
            ,岗位介绍
            ,公司名称
            ,公司行业
            ,公司性质
            ,融资阶段
            ,公司规模
            ,公司主页
            ,发布日期
            ,发布网站
            ,原始URL'''

# 按照文摘3月份最新数据需求定义的字段, 新增了一些字段
# headalias = '''company, firm_type, firm_detail, recruit_type,location, positioin,pacakge, jd, qualification, contact, publish_time, URL'''
# headc = '''公司名称，公司类型，公司介绍，职位名称，工作地点，， 薪水，职位描述，技能要求，联系方式，发布时间，信息来源'''
# headc = '''公司名称，公司类型，公司介绍，招聘类型，工作地点，职位名称， 薪水，职位描述，技能要求，联系方式，发布时间，信息来源'''
# print(head.split(','))
# ['company', ' firm_type', ' type_detail', ' recruit_type', 'location', ' positioin', 'pacakge', ' jd', ' qualification', ' contact', ' publish_time', ' URL']
# table = mongoset('lieping', 'info')
table = mongoset('positiondb', 'posinfo')

# comp_list = ['数据堂','亮风台','图普','图灵','腾云天下','格灵深瞳']
# regcomp = list(map(re.compile, comp_list))

pipeline = [
    {'$match': {'publish_time': {'$gt': '2017-04-03'}}},
    {'$match': {'publish_time': {'$regex': '20'}}},
    {'$match': {'location': {'$in': ['北京', '上海', '广州', '深圳', '杭州']}}},
    {'$match': {'company_name': {'$in': companies}}},
    # {'$match': {'original_site_name': {'$in': ['猎聘','']}}},
    {'$match': {'degree': {'$regex': "[本硕]"}}},
    {'$match': {'crawldetailflag': True}},
    # {'$match': {'year_experience': {'$regex': "[不限]"}}},
    {'$match': {'position_name': {'$regex': "[数据算法AI机器智能虚拟]"}}},
    # #{'age' : {'$in' : [10, 22, 26]}}
    {'$sort': {'year_experience':1}},#{'age' : {'$in' : [10, 22, 26]}}
    # {'$project': {'_id':0,'publish_time':1, 'position_name':1,}},
    # {'$gt': {'publish_time': '2016-12-01'}},
    # {'$match': {'saletime': ''}},
    # {'$match': {'company': {"$in": regcomp}}},
    # {'$group': {'_id': {'$slice': ['$address', 1, 1]}, 'counts': {'$sum': 1}}}
]

redata = []

# table_comp = mongoset('lieping', 'complist')
table_comp = TPOS
# mongoset('openpositiondb', 'complist')

complist = []
#
for item in table_comp.find():
#
    complist.append(item['company'])


time = datetime.now()
filename = 'position' + time.strftime('%Y-%m-%d') + '.xlsx'

redata = []
positionurl = []
# redata.append(headers.split(','))
for item in table.aggregate(pipeline):
    item['position_name'] = ''.join(item['position_name'].split())
    positionurl.append(item['position_url'])
    # 处理薪水, 换算成月薪
    salary = str(item['salary'])
    pt = re.compile(u'(\d*)万')
    if pt.findall(salary):
        match = pt.search(salary)
        smin = int(match.group(1)) / 12 * 10000
        item['salary'] = str(int(smin))

    pt = re.compile(u'(\d*)-(\d*)万')
    if pt.findall(salary):  # .encode('utf-8').decode('utf-8')
        match = pt.search(salary)
        smin = int(match.group(1)) / 12 * 10000
        smax = int(match.group(2)) / 12 * 10000
        item['salary'] = str(int(smin)) + '-' + str(int(smax))


    # 处理日期格式
    try:
        item['publish_time'] = time.strptime(item['publish_time'], '%Y-%m-%d').strftime('%Y/%m/%d')
    except:
        pass
    # 处理公司行业分隔符
    try:
        item['industry'] = ','.join(item['industry'].split('/'))
    except:
        pass

    row = []

    for key in column.split(','):
        try:
            row.append(item[key])

        except:
            row.append('')

    if not row[0] or row[0] != 'None':
        redata.append(row)
        print(row)
print('Total positions are :', len(redata))


# 将筛选后的数据写回数据库, 更新其 crawldetailflag 为True


excelwriter(headers.split(','), redata, filename)

