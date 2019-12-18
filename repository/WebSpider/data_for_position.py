#!usr/bin/env python
# #_*_ coding: utf-8 _*_

import time, re
from datetime import datetime

import pymongo
import csv
from xlswriter import excelwriter
from mongoconn import mongoset, mongoinsert,mongoupdate, TPOS

from companylist import companies

column = 'position_name,' \
         'company_name,' \
         'location,' \
         'year_experience,' \
         'publish_time,' \
         'job_descri,qualification,position_url'

headers = '''职位名称,公司名称,工作地点,工作经验(年),发布日期,工作职责,任职要求,职位链接'''
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


from pipeline import pipeline

redata = []

# table_comp = mongoset('lieping', 'complist')
table_comp = TPOS
# mongoset('openpositiondb', 'complist')

complist = []
#
#


redata = []
positionurl = []
# redata.append(headers.split(','))
for item in table.aggregate(pipeline):
    item['position_name'] = ''.join(item['position_name'].split())
    positionurl.append(item['position_url'])

    #
    try:
        item['job_descri'] = item['qulification']
        # detail = item['job_descri'].split('：')
        pt = re.compile(u'[任职位]{2}要求：(.*)')
        item['qulification'] = pt.search(item['qulification']).group(1)
        pt = re.compile(u'工作职责：(.*)[任职位]{2}要求')
        item['job_descri'] = pt.search(item['job_descri']).group(1)
        # qualification
        # job_decri
        # item['qualification'] = pt.search(item['qualification']).group(1)
    except:
        pass

    # 处理工作经验
    pt = re.compile(u'(\d*)')
    item['year_experience'] = pt.search(item['year_experience']).group(1)


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



time = datetime.now()
filename = 'position' + time.strftime('%Y-%m-%d') + '.xlsx'

excelwriter(headers.split(','), redata, filename)

