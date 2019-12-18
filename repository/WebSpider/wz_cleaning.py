
import time, re
import pymongo

from xlswriter import excelwriter
from mongoconn import mongoset, mongoinsert,mongoupdate


import jieba
import jieba.analyse as fenci

if __name__ == '__main__':
    starttime = time.time()
    print ('start: ')
    print (time.strftime('%Y-%m-%d %H:%M:%S'))

    # TODO first step , get urls of each opened position
    # url = 'https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&key=数据&dqs=020&curPage={}'
    # urlbase = url
    # filternav = 'ul.sojob-list span.job-name a'
    # navurls = get_page_urls(urlbase, '', 3)
    # item_urls = get_item_urls(navurls, filternav, 'div')
    #
    # # store in database
    # mongoinsert(table, listtodict(item_urls))

    # TODO second step
    # separation, there are duplicate words like '的'， '分析'. Using 'set' to remove them

    info = mongoset('lieping', 'info')
    poses = info.find()

    wordbag = []
    for p in poses:
        job_decri = p['job_decri']
        seg_list = jieba.cut(job_decri, cut_all=False)
        words = fenci.extract_tags(job_decri, topK=20, withWeight=False, allowPOS=())
        print(words)
        # words = set(list(seg_list))
        # wordbag += words
    ss = '''岗位职责：
1、负责零售业务经营数据的统计、分析；
2、负责行业经济业务发展的动态跟踪、数据统计、分析；
3、负责零售业务各项营销、激励活动的实施、统计、跟踪；
4、领导安排的其他工作。
任职要求：
1、统计及相关专业，研究生及以上学历；
2、具备良好的沟通协调能力、分析能力和较强的文字功底；
3、具有较强的团队合作意识和责任心。'''
    # seg_list = jieba.cut(ss, cut_all=True)
    #
    #
    # a = set(list(seg_list))

    print(wordbag)
    # TODO statistics analysis

    cc = set(wordbag)
    ww = {}
    for item in cc:
        ww['item'] = wordbag.count(item)

    print(ww)

    ##
    # print(a)
    # print("Full Mode: " + "/ ".join(seg_list))

    # TODO step 3
    # sort the count of each words, choose top 10 or 20 to be the feature


