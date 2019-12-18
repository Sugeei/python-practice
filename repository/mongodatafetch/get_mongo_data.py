
import time, re, datetime
import pymongo
import csv
from xlswriter import excelwriter
from mongoconn import mongoset, mongoinsert,mongoupdate, TPOS

# 2017.03.30
# 按照文摘3月份最新数据需求定义的字段, 新增了一些字段
headalias = [
    'company_name',
    'company_type',
    'company_detail',
    'position_name',
    'position_type',
    'publish_time',
    'location',
    'salary',
    'job_description',
    'qulification',
    'original_site_name',
    '_id',
    'department',
    'industry',
    'company_level',
    'company_url',
    'company_size',
    'company_homepage',
    'year_experience',
    'degree',
    'position_url'

]
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
    # {'$project': {
    #     'company_name': 1,
    #     'company_type': 1,
    #     'company_detail': 1,
    #     'position_name': 1,
    #     'position_type': 0,
    #     'publish_time': 1,
    #     'location':1,
    #     'salary':1,
    #     'job_description':0,
    #     'qulification':0,
    #     'original_site_name':1,
    #     '_id':0,
    #     'department':1,
    #     'industry':1,
    #     'company_level':1,
    #     'company_url':1,
    #     'company_size':1,
    #     'company_homepage':0,
    #     'year_experience':1,
    #     'degree':1,
    #     'position_url':1,
    #
    #     }},
    # {'$match': {'publish_time': {'$gt': '2017-03-27'}}},
    {'$match': {'publish_time': {'$regex': '20'}}},
    # {'$match': {'location': {'$in': ['北京', '上海', '广州', '深圳', '杭州']}}},
    # {'$match': {'degree': {'$regex': "本科"}}},#{'age' : {'$in' : [10, 22, 26]}}
    # {'$sort': },#{'age' : {'$in' : [10, 22, 26]}}
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

# print (complist)

# print(list(table.aggregate(pipeline)))

# comp = []
for item in table.aggregate(pipeline):
    item['position_name'] = ''.join(item['position_name'].split())
    row = []
    for key in headalias:
        try:
            row.append(item[key])
        except:
            row.append('')
    # print(item)
    # if True:
    # # if item['company'] in complist:
    #     redata.append((item['company'], item['firm_type'], '', item['recruit_type'], item['location'],
    #                    item['position'], item['package'], '', '', item['contact_info'],
    #                    item['publish_time'], item['URL']))
        # redata.append((item['company'], item['firm_type'], '', item['recruit_type'], item['location'],
        #                item['position'], item['package'], item['job_decri'], item['qualification'], item['contact_info'],
        #                item['publish_time'], item['URL']))
    print(row)
    redata.append(row)
print('totally get the number of positions is : ', len(redata))
# print(set(comp))
# head = headc.split('，')

time = datetime.datetime.now()
filename = 'position' + time.strftime('%Y-%m-%d') + '.csv'
with open(filename, 'a') as f:
    writer = csv.writer(f)
    writer.writerow(headalias)
    for i in redata:
        writer.writerow(i)

# excelwriter(headalias, redata, filename)

