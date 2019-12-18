 #!usr/bin/env python
#_*_ coding: utf-8 _*_
import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

from requests import request
# from urlparse import  urlparse
import urllib.request as request
from urllib import parse
# import urllib2
from bs4 import BeautifulSoup as Bs
from collections import Counter
# import lxml
import json
import datetime
import xlsxwriter
import re
import requests
import pymongo
from formatdata import formatdata
from mongoconn import mongoset, mongoinsert,mongoupdate

starttime = datetime.datetime.now()

# input('请输入您所需要查找的关键词：')
#获取职位的查询页面，（参数分别为网址，当前页面数，关键词）
def get_page(url, pn, keyword):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
        'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
        'Host': 'www.lagou.com',
        'Connection': 'keep-alive',
        'Origin': 'http://www.lagou.com'
    }
    if pn == 1:
        boo = 'true'
    else:
        boo = 'false'

    proxies = {'http': "207.62.234.53:8118"}
    page_data = parse.urlencode([
        ('first', boo),
        ('pn', pn),
        ('kd', keyword)
    ])
    # page = urllib.request(url, headers=headers)
    req = request.Request(url, headers=headers)
    # 18
    json = request.urlopen(req, data=page_data.encode('utf-8')).read()
    # 19
    data = json.decode('utf-8')
    # 20
    # return page
    # print(url)

    # page = urllib.urlopen(req, data=page_data.encode('utf-8')).read()
    # page = page.decode('utf-8')
    # page = requests.get(url, proxies=proxies, headers=headers)
    return data

def get_format_data(data):
    fdata = {}
    format = ['companyFullName', 'financeStage', '', 'positionName','','createTime','city','salary','']
    selector = {
        'company': 'div.title-info h3 a',
        'firm_type': '',
        'firm_detail': '',
        'position': 'div.title-info h1',
        'recruit_type': '',
        'publish_time': 'div.job-title-left p.basic-infor span',
        'location': 'div.job-title-left p.basic-infor a',
        'package': 'div.job-title-left p.job-item-title',
        'job_decri': 'div.main-message',
        'qualification': 'div.main-message',
        'contact_info': '',
        'original_web': '',
        'URL': '',
    }

    # {
    #     "companyId": 82991,
    #     "adWord": 0,
    #     "positionName": "数据架构师",
    #     "workYear": "1-3年",
    #     "education": "本科",
    #     "jobNature": "全职",
    #     "positionId": 2603070,
    #     "createTime": "2016-12-07 13:59:32",
    #     "companyShortName": "数美",
    #     "score": 0,
    #     "city": "北京",
    #     "salary": "25k-50k",
    #     "approve": 1,
    #     "positionAdvantage": "大数据服务领导者、待遇比肩BAT、全员持股",
    #     "companyLogo": "i/image/M00/76/C2/CgqKkVg2fVCASEreAABS01Upo_A221.jpg",
    #     "district": "朝阳区",
    #     "industryField": "企业服务,数据服务",
    #     "financeStage": "成长型(不需要融资)",
    #     "companyLabelList": ["年底双薪", "大数据", "带薪年假", "通讯津贴"],
    #     "companySize": "50-150人",
    #     "businessZones": ["望京", "来广营", "花家地"],
    #     "imState": "today",
    #     "lastLogin": 1481090352000,
    #     "publisherId": 2117266,
    #     "explain": null,
    #     "plus": null,
    #     "pcShow": 0,
    #     "appShow": 0,
    #     "deliver": 0,
    #     "gradeDescription": null,
    #     "promotionScoreExplain": null,
    #     "firstType": "开发/测试/运维类",
    #     "secondType": "数据开发",
    #     "positionLables": ["资深", "高级", "架构师", "科学家", "数据"],
    #     "companyFullName": "北京数美时代科技有限公司",
    #     "formatCreateTime": "13:59发布"
    # },

def get_position_list(max_pn = 5):
    urlbase = r'http://www.lagou.com/jobs/{}'  # city=%E5%8C%97%E4%BA%AC'
    urlbase = r'https://www.lagou.com/jobs/positionAjax.json?'  # city=%E5%8C%97%E4%BA%AC'
    # urls = ["http://sh.xiaozhu.com/search-duanzufang-p{}-0/".format(pageid) for pageid in range(1, 4)]
    keyword = u'数据'
    urljson = urlbase.format('positionAjax.json?')

    table = mongoset('lieping', 'urls')
    table.create_index([('itemurl', pymongo.DESCENDING)], unique=True)
    tinfo = mongoset('lieping', 'info')

    source = {
        'itemurl': '',
        'flag': False,
    }
    furls = formatdata(source)
    # max_pn = read_max_page(get_page(url, 1, keyword))  # 获取招聘页数
    fin_skill_list = []  # 关键词总表
    for pn in range(1, max_pn):
        # print(('***********************正在抓取第%s页信息***********************' % pn))
        # about json
        # https://pythontips.com/2013/08/08/storing-and-loading-data-with-json/
        page = json.loads(get_page(urljson, pn, keyword))
        itemlist = page["content"]["positionResult"]["result"]
        for item in itemlist:
            url = urlbase.format(str(item["positionId"]) + '.html')
            # TODO write to database
            # for item in item_urls:
            a = furls.getformatdict(['itemurl'], [url])
            print(a)
            # table.insert_one(furls.getformatdict(['itemurl'], [url]))
            try:
                table.insert_one(furls.getformatdict(['itemurl'], [url]))
            except:
                pass

        # company_list = read_id(page)
        # for company_id in company_list:
        #     # content = get_content(company_id)
        #     result = get_result(content)
        #     skill_list = search_skill(result)
        #     fin_skill_list.extend(skill_list)
    # for pi in range(pn):
    #
    #     data = get_page(url, pi, keyword)


#获取所需的岗位ID，每一个招聘页面详情都有一个所属的ID索引
def read_id(page):
    tag = 'positionId'
    page_json = json.loads(page)
    page_json = page_json['content']['positionResult']['result']
    company_list = []
    for i in range(15):
        company_list.append(page_json[i].get(tag))
    return  company_list

# 获取当前招聘关键词的最大页数，大于30的将会被覆盖，所以最多只能抓取30页的招聘信息
def read_max_page(page):
    page_json = json.loads(page)
    max_page_num = page_json['content']['pageSize']
    if max_page_num > 30:
        max_page_num = 30
    return max_page_num

#获取职位页面，由positionId和BaseUrl组合成目标地址
def get_content(company_id):
    fin_url = r'http://www.lagou.com/jobs/%s.html' % company_id
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
        'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
        'Host': 'www.lagou.com',
        'Connection': 'keep-alive',
        'Origin': 'http://www.lagou.com'
    }
    req = request.Request(fin_url, headers=headers)
    #page = urllib.urlopen(req).read()
    page = request.urlopen(req).read()
    content = page.decode('utf-8')
    return content

#获取职位需求（通过re来去除html标记），可以将职位详情单独存储
def get_result(content):
    soup = Bs(content, 'lxml')
    job_description = soup.select('dd[class="job_bt"]')
    job_description = str(job_description[0])
    rule = re.compile(r'<[^>]+>')
    result = rule.sub('', job_description)
    return result

#过滤关键词：目前筛选的方式只是选取英文关键词
def search_skill(result):
    rule = re.compile(r'[a-zA-z]+')
    skil_list = rule.findall(result)
    return skil_list

# 对出现的关键词计数，并排序，选取Top80的关键词作为数据的样本
def count_skill(skill_list):
    for i in range(len(skill_list)):
        skill_list[i] = skill_list[i].lower()
    count_dict = Counter(skill_list).most_common(80)
    return count_dict

# 对结果进行存储并生成Area图
def save_excel(count_dict, file_name):
    book = xlsxwriter.Workbook(r'E:\positions\%s.xls' % file_name)
    tmp = book.add_worksheet()
    row_num = len(count_dict)
    for i in range(1, row_num):
        if i == 1:
            tag_pos = 'A%s' % i
            tmp.write_row(tag_pos, ['关键词', '频次'])
        else:
            con_pos = 'A%s' % i
            k_v = list(count_dict[i-2])
            tmp.write_row(con_pos, k_v)
    chart1 = book.add_chart({'type':'area'})
    chart1.add_series({
        'name' : '=Sheet1!$B$1',
        'categories' : '=Sheet1!$A$2:$A$80',
        'values' : '=Sheet1!$B$2:$B$80'
    })
    chart1.set_title({'name':'关键词排名'})
    chart1.set_x_axis({'name': '关键词'})
    chart1.set_y_axis({'name': '频次(/次)'})
    tmp.insert_chart('C2', chart1, {'x_offset':15, 'y_offset':10})
    book.close()

if __name__ == '__main__':

    get_position_list()
    # max_pn = read_max_page(get_page(url, 1, keyword)) # 获取招聘页数
    # fin_skill_list = [] # 关键词总表
    # for pn in range(1, max_pn):
    #     print(('***********************正在抓取第%s页信息***********************' % pn))
    #     page = get_page(url, pn, keyword)
    #     company_list = read_id(page)
    #     for company_id in company_list:
    #         content = get_content(company_id)
    #         result = get_result(content)
    #         skill_list = search_skill(result)
    #         fin_skill_list.extend(skill_list)
    # print('***********************开始统计关键词出现频率***********************')
    # count_dict = count_skill(fin_skill_list)
    # print(count_dict)
    # file_name = input(r'请输入要保存的文件名：')
    # save_excel(count_dict, file_name)
    # print('***********************正在保存到E:\positions***********************')
    # endtime = datetime.datetime.now()
    # time = (endtime - starttime).seconds
    # print('总共用时：%s s' % time)
