
import time, re
import pymongo

from spider.mongodb_conn import mongoset, mongoinsert,mongoupdate
from spider.database import DBPOS
from spider.pipeline import PIPELINE

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

    # TODO get data
    # separation, there are duplicate words like '的'， '分析'. Using 'set' to remove them
    PIPELINE.append({'$project': {'_id':1,'job_description':1}})

    poses = DBPOS.aggregate(PIPELINE)

    # # TODO get fenci
    # wordbag =[]
    # worddict = {}
    # for p in poses:
    #     job_decri = p['job_description']
    #     seg_list = jieba.cut(job_decri, cut_all=False)
    #     words = fenci.extract_tags(job_decri, topK=20, withWeight=False, allowPOS=())
    #     print(words)
    #     # words = set(list(seg_list))
    #     worddict['id'] = p['_id']
    #     worddict['description'] = ','.join(words)
    #     wordbag.append(worddict)
    # print(wordbag)


    # TODO 分词完成的数据定入csv
    import csv

    with open('jobs.csv', 'w') as csvfile:
        fieldnames = ['id', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # TODO get fenci
        # wordbag = []
        worddict = {}
        for p in poses:
            job_decri = p['job_description']
            seg_list = jieba.cut(job_decri, cut_all=False)
            words = fenci.extract_tags(job_decri, topK=100, withWeight=False, allowPOS=())
            print(words)
            # words = set(list(seg_list))
            worddict['id'] = p['_id']
            worddict['description'] = ','.join(words)
            writer.writerow(worddict)

