#!/usr/bin/python
# -*- coding: UTF-8 -*

#  multiprocess
#  TODO: a spider
#  used to insert a list of position urls into database

from multiprocessing import Pool
import time, re
import pymongo

from mongoconn import mongoset, mongoinsert,mongoupdate
from urlhandler import get_nav_urls, get_page_urls, get_item_urls, get_wrapper,get_soup
from formatdata import formatdata, Fdata
from mongoconn import TURL as table


# get next page 使用while循环一直处理, 采用读取一页list, 处理一页职位item的方式

# 更改策略 拿到 navurls之后 , 发现重复url 则将flag 更新为false, 在get pos info 函数中将Id 赋值为 url + publish time, 以避免重复数据

def get_liepin_list():

    furls = Fdata

    starttime = time.time()
    print ('start: ')
    print (time.strftime('%Y-%m-%d %H:%M:%S'))

    # TODO get urls of each sites with position's urls
    url = 'https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&key=数据&curPage={}'
          # 'https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&key=数据&curPage=0'
    ## url = 'https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&key=数据&curPage=0'
    urlbase = url

    # get urls with different page number
    navurls = get_page_urls(urlbase, '', 3)

    filternav = 'ul.sojob-list span.job-name a'

    # TODO get urls of each opened position
    # return a list with numbers of position's url
    item_urls = get_item_urls(navurls, filternav, 'div')  ## here is where to use spider
    ### item_urls = ['https://www.liepin.com/job/196575988.shtml', 'https://www.liepin.com/job/196472005.shtml', 'https://www.liepin.com/job/196752490.shtml', 'https://www.liepin.com/job/195851461.shtml', 'https://www.liepin.com/job/196502230.shtml', 'https://www.liepin.com/job/194903022.shtml', 'https://www.liepin.com/job/194902934.shtml', 'https://www.liepin.com/job/196531025.shtml', 'https://www.liepin.com/job/196657725.shtml', 'https://www.liepin.com/job/196763924.shtml', 'https://www.liepin.com/job/194827110.shtml', 'https://www.liepin.com/job/196773457.shtml', 'https://www.liepin.com/job/195987062.shtml', 'https://www.liepin.com/job/194505861.shtml', 'https://www.liepin.com/job/195968609.shtml', 'https://www.liepin.com/job/196532604.shtml', 'https://www.liepin.com/job/196532645.shtml', 'https://www.liepin.com/job/196779648.shtml', 'https://www.liepin.com/job/196654991.shtml', 'https://www.liepin.com/job/192423530.shtml', 'https://www.liepin.com/job/196507894.shtml', 'https://www.liepin.com/job/196409648.shtml', 'https://www.liepin.com/job/196749323.shtml', 'https://www.liepin.com/job/196631927.shtml', 'https://www.liepin.com/job/196768016.shtml', 'https://www.liepin.com/job/195134184.shtml', 'https://www.liepin.com/job/196771348.shtml', 'https://www.liepin.com/job/194887589.shtml', 'https://www.liepin.com/job/196708089.shtml', 'https://www.liepin.com/job/196170748.shtml', 'https://www.liepin.com/job/195927926.shtml', 'https://www.liepin.com/job/196409644.shtml', 'https://www.liepin.com/job/196711638.shtml', 'https://www.liepin.com/job/196204557.shtml', 'https://www.liepin.com/job/196741150.shtml', 'https://www.liepin.com/job/195962328.shtml', 'https://www.liepin.com/job/196742070.shtml', 'https://www.liepin.com/job/196744453.shtml', 'https://www.liepin.com/job/196391072.shtml', 'https://www.liepin.com/job/196310194.shtml', 'https://www.liepin.com/job/196384158.shtml', 'https://www.liepin.com/job/196497564.shtml', 'https://www.liepin.com/job/196250649.shtml', 'https://www.liepin.com/job/196764962.shtml', 'https://www.liepin.com/job/196753849.shtml', 'https://www.liepin.com/job/196174521.shtml', 'https://www.liepin.com/job/195820988.shtml', 'https://www.liepin.com/job/196303866.shtml', 'https://www.liepin.com/job/196784172.shtml', 'https://www.liepin.com/job/196784649.shtml', 'https://www.liepin.com/job/196783169.shtml', 'https://www.liepin.com/job/196229720.shtml', 'https://www.liepin.com/job/196783542.shtml', 'https://www.liepin.com/job/196783751.shtml', 'https://www.liepin.com/job/196784072.shtml', 'https://www.liepin.com/job/196783174.shtml', 'https://www.liepin.com/job/196781521.shtml', 'https://www.liepin.com/job/196577603.shtml', 'https://www.liepin.com/job/196775021.shtml', 'https://www.liepin.com/job/196783750.shtml', 'https://www.liepin.com/job/196666499.shtml', 'https://www.liepin.com/job/196225705.shtml', 'https://www.liepin.com/job/196225706.shtml', 'https://www.liepin.com/job/195207349.shtml', 'https://www.liepin.com/job/196730372.shtml', 'https://www.liepin.com/job/196075687.shtml', 'https://www.liepin.com/job/195702461.shtml', 'https://www.liepin.com/job/196158888.shtml', 'https://www.liepin.com/job/196413940.shtml', 'https://www.liepin.com/job/196531966.shtml', 'https://www.liepin.com/job/196786218.shtml', 'https://www.liepin.com/job/196754296.shtml', 'https://www.liepin.com/job/195098560.shtml', 'https://www.liepin.com/job/196448465.shtml', 'https://www.liepin.com/job/196727630.shtml', 'https://www.liepin.com/job/195843043.shtml', 'https://www.liepin.com/job/196205313.shtml', 'https://www.liepin.com/job/195449775.shtml', 'https://www.liepin.com/job/196707054.shtml', 'https://www.liepin.com/job/195557051.shtml', 'https://www.liepin.com/job/196075366.shtml', 'https://www.liepin.com/job/196785705.shtml', 'https://www.liepin.com/job/196656703.shtml', 'https://www.liepin.com/job/195358387.shtml', 'https://www.liepin.com/job/196470403.shtml', 'https://www.liepin.com/job/196789522.shtml', 'https://www.liepin.com/job/194991218.shtml', 'https://www.liepin.com/job/196789380.shtml', 'https://www.liepin.com/job/196789387.shtml', 'https://www.liepin.com/job/196289733.shtml', 'https://www.liepin.com/job/196783138.shtml', 'https://www.liepin.com/job/196785001.shtml', 'https://www.liepin.com/job/194965749.shtml', 'https://www.liepin.com/job/196289723.shtml', 'https://www.liepin.com/job/196679294.shtml', 'https://www.liepin.com/job/196116875.shtml', 'https://www.liepin.com/job/194543479.shtml', 'https://www.liepin.com/job/195131818.shtml', 'https://www.liepin.com/job/196138359.shtml', 'https://www.liepin.com/job/194543486.shtml', 'https://www.liepin.com/job/194543468.shtml', 'https://www.liepin.com/job/196246947.shtml', 'https://www.liepin.com/job/196679293.shtml', 'https://www.liepin.com/job/194774544.shtml', 'https://www.liepin.com/job/196660850.shtml', 'https://www.liepin.com/job/196679292.shtml', 'https://www.liepin.com/job/195131843.shtml', 'https://www.liepin.com/job/196785367.shtml', 'https://www.liepin.com/job/196037222.shtml', 'https://www.liepin.com/job/196129155.shtml', 'https://www.liepin.com/job/196063361.shtml', 'https://www.liepin.com/job/196752999.shtml', 'https://www.liepin.com/job/196753107.shtml', 'https://www.liepin.com/job/196752799.shtml', 'https://www.liepin.com/job/196561506.shtml', 'https://www.liepin.com/job/196315479.shtml', 'https://www.liepin.com/job/196752954.shtml', 'https://www.liepin.com/job/196789916.shtml', 'https://www.liepin.com/job/196551203.shtml', 'https://www.liepin.com/job/196553720.shtml', 'https://www.liepin.com/job/196553722.shtml', 'https://www.liepin.com/job/196727615.shtml', 'https://www.liepin.com/job/196783291.shtml', 'https://www.liepin.com/job/195089521.shtml', 'https://www.liepin.com/job/196784650.shtml', 'https://www.liepin.com/job/196784900.shtml', 'https://www.liepin.com/job/196634520.shtml', 'https://www.liepin.com/job/196782721.shtml', 'https://www.liepin.com/job/196189281.shtml', 'https://www.liepin.com/job/196322850.shtml', 'https://www.liepin.com/job/196450230.shtml', 'https://www.liepin.com/job/196140371.shtml', 'https://www.liepin.com/job/194962767.shtml', 'https://www.liepin.com/job/196382779.shtml', 'https://www.liepin.com/job/196782453.shtml', 'https://www.liepin.com/job/196783583.shtml', 'https://www.liepin.com/job/196280741.shtml', 'https://www.liepin.com/job/196782558.shtml', 'https://www.liepin.com/job/196182229.shtml', 'https://www.liepin.com/job/196782559.shtml', 'https://www.liepin.com/job/196783156.shtml', 'https://www.liepin.com/job/196580187.shtml', 'https://www.liepin.com/job/196783616.shtml', 'https://www.liepin.com/job/196785819.shtml', 'https://www.liepin.com/job/196535411.shtml', 'https://www.liepin.com/job/196786223.shtml', 'https://www.liepin.com/job/196591583.shtml', 'https://www.liepin.com/job/196542349.shtml', 'https://www.liepin.com/job/196784169.shtml', 'https://www.liepin.com/job/194779743.shtml', 'https://www.liepin.com/job/196783816.shtml', 'https://www.liepin.com/job/196785725.shtml', 'https://www.liepin.com/job/196610531.shtml', 'https://www.liepin.com/job/196170495.shtml', 'https://www.liepin.com/job/196715818.shtml', 'https://www.liepin.com/job/196705435.shtml', 'https://www.liepin.com/job/196702378.shtml', 'https://www.liepin.com/job/196170361.shtml']
    #

    # TODO write to database
    dupflag = 0
    # table.insert_one(furls.getformatdict(['itemurl'], [item_urls[0]])) ## 并非重复数据为什么报数据重复的错误？ ？？
    for item in item_urls:
         # to record how many duplication records found
        try:
            table.insert_one(furls.getformatdict(['itemurl','_id'], [item, item]))
        # except pymongo.errors.DuplicateKeyError:
        #     dupflag += 1
        except:
            table.update_one({'itemurl': url}, {'$set': {'flag': False}})
            pass

def get_item_urls(urls, filter, filtervalid=''):

    itemurls = []
    for url in urls:
        sleeptime = random.randint(5, 15)
        soup = get_soup(url)
        # print('start search ' + url)
        if len(soup.select(filtervalid)):
            itemlist = soup.select(filter)
            if len(itemlist):
                for item in itemlist:
                    try:
                        itemurl = item.get('href')
                    except:
                        pass
                    itemurls.append(itemurl)
        # print('sleep ' + str(sleeptime) + 's')
        time.sleep(sleeptime)
    print('[Note]totally ' + str(len(itemurls)) + ' positions found' )
    return itemurls

if __name__ == '__main__':


    furls = Fdata

    starttime = time.time()
    print ('start: ')
    print (time.strftime('%Y-%m-%d %H:%M:%S'))

    # TODO get urls of each sites with position's urls
    url = 'https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&key=数据&curPage={}'
          # 'https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&key=数据&curPage=0'
    ## url = 'https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&key=数据&curPage=0'
    urlbase = url
    for i in range(1,15):
        soup = get_soup(url.format(i))

    # get urls with different page number
    navurls = get_page_urls(urlbase, '', 3)

    filternav = 'ul.sojob-list span.job-name a'

    # TODO get urls of each opened position
    # return a list with numbers of position's url
    item_urls = get_item_urls(navurls, filternav, 'div')  ## here is where to use spider
    ### item_urls = ['https://www.liepin.com/job/196575988.shtml', 'https://www.liepin.com/job/196472005.shtml', 'https://www.liepin.com/job/196752490.shtml', 'https://www.liepin.com/job/195851461.shtml', 'https://www.liepin.com/job/196502230.shtml', 'https://www.liepin.com/job/194903022.shtml', 'https://www.liepin.com/job/194902934.shtml', 'https://www.liepin.com/job/196531025.shtml', 'https://www.liepin.com/job/196657725.shtml', 'https://www.liepin.com/job/196763924.shtml', 'https://www.liepin.com/job/194827110.shtml', 'https://www.liepin.com/job/196773457.shtml', 'https://www.liepin.com/job/195987062.shtml', 'https://www.liepin.com/job/194505861.shtml', 'https://www.liepin.com/job/195968609.shtml', 'https://www.liepin.com/job/196532604.shtml', 'https://www.liepin.com/job/196532645.shtml', 'https://www.liepin.com/job/196779648.shtml', 'https://www.liepin.com/job/196654991.shtml', 'https://www.liepin.com/job/192423530.shtml', 'https://www.liepin.com/job/196507894.shtml', 'https://www.liepin.com/job/196409648.shtml', 'https://www.liepin.com/job/196749323.shtml', 'https://www.liepin.com/job/196631927.shtml', 'https://www.liepin.com/job/196768016.shtml', 'https://www.liepin.com/job/195134184.shtml', 'https://www.liepin.com/job/196771348.shtml', 'https://www.liepin.com/job/194887589.shtml', 'https://www.liepin.com/job/196708089.shtml', 'https://www.liepin.com/job/196170748.shtml', 'https://www.liepin.com/job/195927926.shtml', 'https://www.liepin.com/job/196409644.shtml', 'https://www.liepin.com/job/196711638.shtml', 'https://www.liepin.com/job/196204557.shtml', 'https://www.liepin.com/job/196741150.shtml', 'https://www.liepin.com/job/195962328.shtml', 'https://www.liepin.com/job/196742070.shtml', 'https://www.liepin.com/job/196744453.shtml', 'https://www.liepin.com/job/196391072.shtml', 'https://www.liepin.com/job/196310194.shtml', 'https://www.liepin.com/job/196384158.shtml', 'https://www.liepin.com/job/196497564.shtml', 'https://www.liepin.com/job/196250649.shtml', 'https://www.liepin.com/job/196764962.shtml', 'https://www.liepin.com/job/196753849.shtml', 'https://www.liepin.com/job/196174521.shtml', 'https://www.liepin.com/job/195820988.shtml', 'https://www.liepin.com/job/196303866.shtml', 'https://www.liepin.com/job/196784172.shtml', 'https://www.liepin.com/job/196784649.shtml', 'https://www.liepin.com/job/196783169.shtml', 'https://www.liepin.com/job/196229720.shtml', 'https://www.liepin.com/job/196783542.shtml', 'https://www.liepin.com/job/196783751.shtml', 'https://www.liepin.com/job/196784072.shtml', 'https://www.liepin.com/job/196783174.shtml', 'https://www.liepin.com/job/196781521.shtml', 'https://www.liepin.com/job/196577603.shtml', 'https://www.liepin.com/job/196775021.shtml', 'https://www.liepin.com/job/196783750.shtml', 'https://www.liepin.com/job/196666499.shtml', 'https://www.liepin.com/job/196225705.shtml', 'https://www.liepin.com/job/196225706.shtml', 'https://www.liepin.com/job/195207349.shtml', 'https://www.liepin.com/job/196730372.shtml', 'https://www.liepin.com/job/196075687.shtml', 'https://www.liepin.com/job/195702461.shtml', 'https://www.liepin.com/job/196158888.shtml', 'https://www.liepin.com/job/196413940.shtml', 'https://www.liepin.com/job/196531966.shtml', 'https://www.liepin.com/job/196786218.shtml', 'https://www.liepin.com/job/196754296.shtml', 'https://www.liepin.com/job/195098560.shtml', 'https://www.liepin.com/job/196448465.shtml', 'https://www.liepin.com/job/196727630.shtml', 'https://www.liepin.com/job/195843043.shtml', 'https://www.liepin.com/job/196205313.shtml', 'https://www.liepin.com/job/195449775.shtml', 'https://www.liepin.com/job/196707054.shtml', 'https://www.liepin.com/job/195557051.shtml', 'https://www.liepin.com/job/196075366.shtml', 'https://www.liepin.com/job/196785705.shtml', 'https://www.liepin.com/job/196656703.shtml', 'https://www.liepin.com/job/195358387.shtml', 'https://www.liepin.com/job/196470403.shtml', 'https://www.liepin.com/job/196789522.shtml', 'https://www.liepin.com/job/194991218.shtml', 'https://www.liepin.com/job/196789380.shtml', 'https://www.liepin.com/job/196789387.shtml', 'https://www.liepin.com/job/196289733.shtml', 'https://www.liepin.com/job/196783138.shtml', 'https://www.liepin.com/job/196785001.shtml', 'https://www.liepin.com/job/194965749.shtml', 'https://www.liepin.com/job/196289723.shtml', 'https://www.liepin.com/job/196679294.shtml', 'https://www.liepin.com/job/196116875.shtml', 'https://www.liepin.com/job/194543479.shtml', 'https://www.liepin.com/job/195131818.shtml', 'https://www.liepin.com/job/196138359.shtml', 'https://www.liepin.com/job/194543486.shtml', 'https://www.liepin.com/job/194543468.shtml', 'https://www.liepin.com/job/196246947.shtml', 'https://www.liepin.com/job/196679293.shtml', 'https://www.liepin.com/job/194774544.shtml', 'https://www.liepin.com/job/196660850.shtml', 'https://www.liepin.com/job/196679292.shtml', 'https://www.liepin.com/job/195131843.shtml', 'https://www.liepin.com/job/196785367.shtml', 'https://www.liepin.com/job/196037222.shtml', 'https://www.liepin.com/job/196129155.shtml', 'https://www.liepin.com/job/196063361.shtml', 'https://www.liepin.com/job/196752999.shtml', 'https://www.liepin.com/job/196753107.shtml', 'https://www.liepin.com/job/196752799.shtml', 'https://www.liepin.com/job/196561506.shtml', 'https://www.liepin.com/job/196315479.shtml', 'https://www.liepin.com/job/196752954.shtml', 'https://www.liepin.com/job/196789916.shtml', 'https://www.liepin.com/job/196551203.shtml', 'https://www.liepin.com/job/196553720.shtml', 'https://www.liepin.com/job/196553722.shtml', 'https://www.liepin.com/job/196727615.shtml', 'https://www.liepin.com/job/196783291.shtml', 'https://www.liepin.com/job/195089521.shtml', 'https://www.liepin.com/job/196784650.shtml', 'https://www.liepin.com/job/196784900.shtml', 'https://www.liepin.com/job/196634520.shtml', 'https://www.liepin.com/job/196782721.shtml', 'https://www.liepin.com/job/196189281.shtml', 'https://www.liepin.com/job/196322850.shtml', 'https://www.liepin.com/job/196450230.shtml', 'https://www.liepin.com/job/196140371.shtml', 'https://www.liepin.com/job/194962767.shtml', 'https://www.liepin.com/job/196382779.shtml', 'https://www.liepin.com/job/196782453.shtml', 'https://www.liepin.com/job/196783583.shtml', 'https://www.liepin.com/job/196280741.shtml', 'https://www.liepin.com/job/196782558.shtml', 'https://www.liepin.com/job/196182229.shtml', 'https://www.liepin.com/job/196782559.shtml', 'https://www.liepin.com/job/196783156.shtml', 'https://www.liepin.com/job/196580187.shtml', 'https://www.liepin.com/job/196783616.shtml', 'https://www.liepin.com/job/196785819.shtml', 'https://www.liepin.com/job/196535411.shtml', 'https://www.liepin.com/job/196786223.shtml', 'https://www.liepin.com/job/196591583.shtml', 'https://www.liepin.com/job/196542349.shtml', 'https://www.liepin.com/job/196784169.shtml', 'https://www.liepin.com/job/194779743.shtml', 'https://www.liepin.com/job/196783816.shtml', 'https://www.liepin.com/job/196785725.shtml', 'https://www.liepin.com/job/196610531.shtml', 'https://www.liepin.com/job/196170495.shtml', 'https://www.liepin.com/job/196715818.shtml', 'https://www.liepin.com/job/196705435.shtml', 'https://www.liepin.com/job/196702378.shtml', 'https://www.liepin.com/job/196170361.shtml']
    #

    # TODO write to database
    dupflag = 0
    # table.insert_one(furls.getformatdict(['itemurl'], [item_urls[0]])) ## 并非重复数据为什么报数据重复的错误？ ？？
    for item in item_urls:
         # to record how many duplication records found
        try:
            table.insert_one(furls.getformatdict(['itemurl','_id'], [item, item]))
        # except pymongo.errors.DuplicateKeyError:
        #     dupflag += 1
        except:
            table.update_one({'itemurl': url}, {'$set': {'flag': False}})
            pass



