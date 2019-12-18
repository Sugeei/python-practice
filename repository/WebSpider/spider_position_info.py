#!/usr/bin/python
# -*- coding: UTF-8 -*

#  multiprocess
#  TODO: a spider goes to lieping.com
#  信息分类存储

from multiprocessing import Pool
import time, re, random
import pymongo


from mongoconn import mongoset, mongoinsert,mongoupdate
from urlhandler import get_nav_urls, get_page_urls, get_item_urls, get_wrapper, get_soup

from mongoconn import TURL as urls
from mongoconn import TPOS as tinfo

from DataSelector import dataFactory

if __name__ == '__main__':

    # table = mongoset('openpositiondb', 'urllist')
    #
    # tinfo = mongoset('openpositiondb', 'positions')
    # tinfo.create_index([('URL', pymongo.DESCENDING)], unique=True)
    countinfo = tinfo.count()
    starttime = time.time()
    print ('start: ')
    print (time.strftime('%Y-%m-%d %H:%M:%S'))

    # TODO second step

    # urls = mongoset('openpositiondb', 'urllist')
    urllist = urls.find({'flag':False})
    # urllist = urls.find()
    if not urllist:
        print('''no updated in table 'urls' ''')

    infobag = []
    # urllist = ['https://www.lagou.com/jobs/938099.html','https://www.liepin.com/job/196785097.shtml']
    for item in urllist:
        # print (item)
        url = item['itemurl']
        print(url)
        sleeptime = random.randint(5, 20)
        factory = dataFactory()
        # pattern = re.compile('www\.(.*)\.com')
        # webflag = pattern.findall(item, 1)
        webflag = re.search(r'www\.(.*)\.com',url).group(1)
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
            data['URL'] = url
            data['_id'] = data['URL'] + data['publish_time']
            print(data)
            # tinfo.insert_one(data)
            # countinfo_after = tinfo.count()
            # print('inserted data: ' + str(countinfo_after - countinfo))
            try:
               tinfo.insert_one(data)
               countinfo_after = tinfo.count()
               print('inserted data: ' + str(countinfo_after - countinfo))
               urls.update_one({'itemurl': url}, {'$set': {'flag': True}})

            except pymongo.errors.DuplicateKeyError:
                urls.update_one({'itemurl': url}, {'$set': {'flag': True}})
            except:
                pass
            # urls.update_one({'itemurl': url}, {'$set': {'flag': True}})
        else:
            urls.update_one({'itemurl': url}, {'$set': {'flag': True}})
        print('I will sleep ' + str(sleeptime) + 's')
        time.sleep(sleeptime)

    print('end: ')
    endtime = time.time()
    print (time.strftime('%Y-%m-%d %H:%M:%S'))
    elapsed = endtime - starttime

    countinfo_after = tinfo.count()
    print('Totally inserted data: ' + str(countinfo_after-countinfo))