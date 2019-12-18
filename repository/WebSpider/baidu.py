# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
from datetime import datetime
from bs4 import BeautifulSoup
from mongoconn import mongoset
from user_agent import ua
import random


c = datetime.now()

def write_to_file(html):
    with open('log_' + str(c.strftime('%Y-%m-%d %H:%M:%S')) + '_soup.html', 'w') as fh:
        try:
            fh.write(html[0].text.decode("gbk"))
        except:
            pass

class HtmlParser(object):

    def __init__(self, soup, keyword):
        self.soup = soup
        self.keyword = keyword
        self.timestamp = ''
        self.dbconn = mongoset('datacourse', 'advertiserinfo')

    def _insert_one(self,item):
        # item = [i.replace(',', '.') for i in item.values()]
        for key, value in item.items():
            try:
                item[key] = value.replace(',', '.')
            except:
                pass
        # if item["coursetitle"]:
        try:
            self.dbconn.insert_one(item)
        except:
            pass

    def insert_data(self):
        curtime = datetime.now()
        self.timestamp = str(curtime.strftime('%Y-%m-%d %H:%M:%S'))

        for item in self._get_left_lsit():

            self._insert_one(item)

        for item in self._get_left_result_list():
            self._insert_one(item)

        for item in self._get_right_list():
            self._insert_one(item)

        self._insert_one(self._get_right_adver())

    def _get_left_lsit(self):
        #  AD list
        divlist = self.soup.select('#content_left > div')

        adtitle = []
        adurl = []
        for ad in divlist:
            title = ad.select('div > h3.t > a')
            for t in title:
                adtitle.append(t.text)
                # print(t.text)
            url = ad.select('div > a > span')
            for u in url:
                # print(u.text)
                adurl.append(u.text)

        item = {}
        for i in range(len(adtitle)):
            item["_id"] = self.timestamp + ' ' + adurl[i]
            item["keyword"] = self.keyword
            item["ad_location"] = 'content_left'
            item["index"] = i
            item["is_advertise"] = True
            item["timestamp"] = self.timestamp
            item["coursetitle"] = adtitle[i]
            item["courseurl"] = adurl[i]
            yield item
            # self.dbconn.insert_one(item)

    def _get_left_result_list(self):
        divlist = self.soup.select('#content_left > div.result')
        adtitle = []
        adurl = []
        for resulit in divlist:
            title = resulit.select('h3.t > a')
            for t in title:
                adtitle.append(t.text)
                # print(t.text)
            url = resulit.select('div.f13 > a')[0:1]
            for u in url:
                # print(u.text)
                adurl.append(u.text)

        item = {}
        for i in range(len(adtitle)):
            item["_id"] = self.timestamp + ' ' + adurl[i]
            item["keyword"] = self.keyword
            item["ad_location"] = 'content_left'
            item["index"] = i
            item["is_advertise"] = False
            item["timestamp"] = self.timestamp
            item["coursetitle"] = adtitle[i]
            item["courseurl"] = adurl[i]
            yield item
            # datacourseinfo.insert_one(item)
            # try:
            #     datacourseinfo.insert_one(item)
            # except:
            #     pass

    def _get_right_adver(self):
        # content_right
        item = {}
        r_title = self.soup.select('div#content_right p a')
        # for title in r_title:
        if r_title:
            title = r_title[0]
            if title.text:
                item["_id"] = self.timestamp + ' 品牌广告'
                item["keyword"] = self.keyword
                item["ad_location"] = 'content_right'
                item["index"] = '品牌广告'
                item["is_advertise"] = True
                item["timestamp"] = self.timestamp
                item["coursetitle"] = title.text
                item["courseurl"] = ''
        return item

    def _get_right_list(self):
        item = {}
        recommends = self.soup.select('div.content_right div.opr-recommends-merge-mbGap')  # div.opr-recommends-merge-item')
        for tag in recommends:
            title = tag.select('div.c-gap-top-small a')  # .text
            item["_id"] = self.timestamp + ' 推荐' + title
            item["keyword"] = self.keyword
            item["ad_location"] = 'recommend'
            item["index"] = '相关企业'
            item["is_advertise"] = True
            item["timestamp"] = self.timestamp
            item["coursetitle"] = title
            item["courseurl"] = ''
            yield item

class Crawler(object):
    # get response from server
    def __init__(self, keyword):
        self.keyword = keyword

    def get_html(self):
        s = urllib.parse.quote(self.keyword)
        url = 'https://www.baidu.com/s?wd=%s' % (s)

        urllib.request.urlopen(url)
        idx = random.randint(0, len(ua) - 1)
        req = urllib.request.Request(url, headers={
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': ua[idx]  # 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
        })
        response = urllib.request.urlopen(req)
        # response = requests.get()
        soup = BeautifulSoup(response.read(), "lxml")
        return soup

s='大数据培训'
crawler = Crawler(s)
soup = crawler.get_html()
# write_to_file(soup.select('div#content_right'))
parser = HtmlParser(soup,s)
parser.insert_data()

s='大数据 培训'
crawler = Crawler(s)
soup = crawler.get_html()
# write_to_file(soup.select('div#content_right'))
parser = HtmlParser(soup,s)
parser.insert_data()
