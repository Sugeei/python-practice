
import time, re, datetime
import pymongo

from xlswriter import excelwriter
from mongoconn import mongoset, mongoinsert,mongoupdate, TPOS

headalias = '''company, firm_type, firm_detail, recruit_type,location, positioin,pacakge, jd, qualification, contact, publish_time, URL'''
headc = '''公司名称，公司类型，公司介绍，招聘类型，工作地点，职位名称， 薪水，职位描述，技能要求，联系方式，发布时间，信息来源'''
# print(head.split(','))
# ['company', ' firm_type', ' type_detail', ' recruit_type', 'location', ' positioin', 'pacakge', ' jd', ' qualification', ' contact', ' publish_time', ' URL']
# table = mongoset('lieping', 'info')
table = mongoset('openpositiondb', 'positions')

# comp_list = ['数据堂','亮风台','图普','图灵','腾云天下','格灵深瞳']
# regcomp = list(map(re.compile, comp_list))

pipeline = [
    {'$match': {'publish_time': {'$gt': '2017-02-01'}}},
    {'$project': {'_id':0,'publish_time':1, 'position_name':1,}},
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
# for item in table_comp.find():
#
#     complist.append(item['company'])

# print (complist)

# print(list(table.aggregate(pipeline)))

# comp = []
for item in table.aggregate(pipeline):
    # comp.append(item['company'])
    # item = {
    #     'name': i['_id'][0] + '' + str(int(float(i['counts'] / salesum) * 10000) / 100) + '%',
    #     'y': int(float(i['counts'] / salesum) * 10000) / 100,
    #     'type': 'pie'
    # }

    # with all the columns
    # redata.append((item['company'], item['firm_type'], item['firm_detail'], item['recruit_type'], item['location'],
    #                item['position'], item['package'], item['job_decri'], item['qualification'], item['contact_info'],
    #                item['publish_time'], item['URL']))

    # with no firm detail
    print(item)
    # if True:
    # # if item['company'] in complist:
    #     redata.append((item['company_name'], item['firm_type'], '', item['recruit_type'], item['location'],
    #                    item['position'], item['package'], item['job_decri'], item['qualification'], item['contact_info'],
    #                    item['publish_time'], item['URL']))
    # # redata.append((item['company'], item['firm_type'], item['firm_detail'], item['recruit_type'], item['location'], item['position'], item['package'], item['job_decri'], item['qualification'], item['contact_info'], item['publish_time'], item['URL']))
# print(set(comp))
head = headc.split('，')

time = datetime.datetime.now()
filename = 'position' + time.strftime('%Y-%m-%d') + '.xlsx'
excelwriter(head, redata, filename)

