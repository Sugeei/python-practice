#!usr/bin/env python
# #_*_ coding: utf-8 _*_

import time, re
from datetime import datetime

import pymongo
import csv
from xlswriter import excelwriter
from mongoconn import mongoset, mongoinsert,mongoupdate, TPOS

# from companylist import companies

import time, re, random
import pymongo


from mongoconn import mongoset, mongoinsert,mongoupdate
from urlhandler import get_nav_urls, get_page_urls, get_item_urls, get_wrapper, get_soup

from mongoconn import TURL as urls
from mongoconn import TPOS as tinfo

from DataSelector import dataFactory

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

from pipeline import pipeline

redata = []

# table_comp = mongoset('lieping', 'complist')
table_comp = TPOS
# mongoset('openpositiondb', 'complist')

complist = []
#
# for item in table_comp.find():
#
    # complist.append(item['company'])


curtime = datetime.now()
filename = 'position' + curtime.strftime('%Y-%m-%d') + '.xlsx'

redata = []
positionurl = []
# redata.append(headers.split(','))
# 获取 crawldetailflag 为True 的数据的 detail 职位详情页
import random
for item in table.aggregate(pipeline):
    item['position_name'] = ''.join(item['position_name'].split())
    positionurl.append(item['position_url'])

    url = item['position_url']
    print(url)
    sleeptime = random.randint(5, 20)
    factory = dataFactory()
    # pattern = re.compile('www\.(.*)\.com')
    # webflag = pattern.findall(item, 1)
    webflag = re.search(r'www\.(.*)\.com', url).group(1)
    webitem = factory.dataselector(webflag, '', '')
    soup = get_soup(url)
    # soup = get_wrapper(item, 'div.about-position')
    # pattern = re.compile(r'404')
    # TODO 从读到的soup中尝获取目标字段
    data = ''
    try:
        data = webitem.get_formated_data(soup)
    except:
        pass
    # TODO 如果data为空，说明此网页过期或者访问失败，则跳过以下步骤，并将此url标记为已访问
    if data:
        # print(url)
        # data['URL'] = url
        # data['_id'] = data['URL'] + data['publish_time']
        print(data)
        # tinfo.insert_one(data)
        # countinfo_after = tinfo.count()
        # print('inserted data: ' + str(countinfo_after - countinfo))
        try:
            # countinfo_after = tinfo.count()
            tinfo.update_one({'_id': item['_id']}, {'$set': {'qulification': data['qualification']}})
            tinfo.update_one({'_id': item['_id']}, {'$set': {'crawldetailflag': False}})
            # print('inserted data: ' + str(countinfo_after - countinfo))

        except pymongo.errors.DuplicateKeyError:
            pass
        except:
            pass
            # urls.update_one({'itemurl': url}, {'$set': {'flag': True}})
    time.sleep(sleeptime)
    print('sleep:' , sleeptime, 's')


# print('Total positions are :', len(redata))


# 将筛选后的数据写回数据库, 更新其 crawldetailflag 为True



# excelwriter(headers.split(','), redata, filename)

