import scrapy
import pymongo
import re
import datetime
import time, random
from datetime import datetime, timedelta
from wenzhaispider.items import ITEMKEYS, BosssPositionItem, PosInfoItem
from scrapy.conf import settings


class PositionInfoSpider(scrapy.Spider):

    name = "temp"

    def start_requests(self):
        # # boss zhipin
        # urlt = 'https://www.bosszhipin.com/niuren/joblist.html?key={}'
        # pos = u'数据'
        # url = urlt.format(pos)
        # yield scrapy.Request(url=url, callback=self.parse_boss)

        # liepin
        url = 'https://www.liepin.com/zhaopin/?key=数据'
        ## url = 'https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&key=数据&curPage=0'
        yield scrapy.Request(url=url, callback=self.parse_liepin)
        #
        # # zhilian
        # url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?kw=数据'
        # yield scrapy.Request(url=url, callback=self.parse_zhilian)

    def parse_liepin(self, response):
        # resitem = BosssPositionItem()
        for item in response.xpath('//div[@class="sojob-item-main clearfix"]/div[@class="job-info"]/span[@class="job-name"]/a/@href').extract():
            # resitem['posid'] = response.urljoin(item) #.extract()
            # resitem['flag'] = False
            # BosssPositionItem['flag'] = False # not visited yet
            yield scrapy.Request(item, callback=self.parse_liepin_pos_info)
            print(item)

            time.sleep(random.randint(1,5))

        # follow pagination links
        flag = 0
        next_page = response.xpath('//div[@class="pagerbar"]/a[text()="下一页"]/@href').extract_first()
        if next_page is not None and flag<3:
            # next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_liepin)
            flag += 1

    def parse_liepin_pos_info(self, response):
        # 'https://www.liepin.com/job/192002405.shtml'
        info = PosInfoItem()
        filter = {
            'company': 'div.title-info h3 a::text',
            'firm_type': '',
            'firm_detail': '',
            'position': 'div.title-info h1::text',
            'recruit_type': '',
            'publish_time': '',
            'location': 'div.job-title-left p.basic-infor span a::text',
            'package': 'div.job-title-left p.job-item-title::text',
            'job_decri': '',
            'qualification': '',
            'contact_info': '',
            'original_web': '',
            'URL': '',
        }.values()
        filter = [
            'div.title-info h3 a::text','','','div.title-info h1::text','','',
            'div.job-title-left p.basic-infor span a::text',
            'div.job-title-left p.job-item-title::text','','','','',''
        ]

        # info['job_decri'] = ' '.join(response.css('div.main-message div.content::text').extract())
        for fi in range(len(ITEMKEYS)):
            # if not filter[fi]:
            #     info[ITEMKEYS[fi]] = ''
            # else:
            info[ITEMKEYS[fi]] = response.css(filter[fi]).extract_first()
            if info[ITEMKEYS[fi]]:
                info[ITEMKEYS[fi]] = info[ITEMKEYS[fi]].strip('\t').strip('\r').strip('\n')
            else:
                info[ITEMKEYS[fi]] = ''

        try:
            info['publish_time'] = response.css('div.job-title-left p.basic-infor span::text').extract()[4]
        except:
            pass

        try:
            pub_t = info['publish_time'] #getemtext(soup.select('div.job-title-left p.basic-infor span')[1])
            # print(pub_t)
            timenow = datetime.now()
            if re.match('\d*-\d*-\d', pub_t):
                info['publish_time'] = pub_t
            # formattime = pub_t
            else:
                formattime = timenow
                # pt = re.compile(u'刚刚')
                # if pt.findall(pub_t): formattime = timenow
                pt = re.compile(u'小时前')
                if pt.findall(pub_t):
                    hrs = re.search('\d*', pub_t)
                    formattime = timenow - timedelta(hours=int(hrs.group(0)))
                pt = re.compile(u'昨天')
                if pt.findall(pub_t): formattime = timenow - timedelta(days=1)
                pt = re.compile(u'前天')
                if pt.findall(pub_t):
                    formattime = timenow - timedelta(days=2)
                info['publish_time'] = formattime.strftime('%Y-%m-%d')
        except:
            pass

        try:
            info['job_description'] = ' '.join(response.css('div.main-message div.content::text').extract())
            info['qulification'] = ' '.join(response.css('div.main-message div.content::text').extract())
        except:
            pass
        info['original_site_name'] = u'猎聘'
        info['_id'] = response.url
        # a=soup.select(filter['job_decri'])[1]
        print(info)
        if info:
            return info
        # else:
        #     raise CloseSpider('no info')


    def parse_zhilian(self, response):

        # resitem = BosssPositionItem()
        for item in response.css('td.zwmc div a::attr("href")').extract():
            # resitem['posid'] = response.urljoin(item) #.extract()
            # resitem['flag'] = False
            # BosssPositionItem['flag'] = False # not visited yet
            yield scrapy.Request(item, callback=self.parse_zhilian_pos_info)


    def parse_zhilian_pos_info(self, response):
        # http://jobs.zhaopin.com/387228188250004.htm
        info = PosInfoItem()

        # posurls = response.css('td.zwmc div a::attr("href")').extract()

        filter = {
            'company': 'div.inner-left h2 a::text',
            'firm_type': '',
            'firm_detail': '',
            'position': 'div.inner-left h1::text',
            'recruit_type': '',
            'publish_time': 'ul.terminal-ul li strong span::text',
            'location': 'ul.terminal-ul li a::text',
            'package': 'ul.terminal-ul li strong::text',
            'job_decri': '',
            'qualification': '',
            'contact_info': '',
            'original_web': '',
            'URL': '',
        }.values()
        filter = [
            'div.inner-left h2 a::text','','','div.inner-left h1::text','','ul.terminal-ul li strong span::text',
            'ul.terminal-ul li a::text',
            'ul.terminal-ul li strong::text','','','','',''
        ]

        # info['job_decri'] = ' '.join(response.css('div.main-message div.content::text').extract())
        for fi in range(len(ITEMKEYS)):
            if not filter[fi]:
                info[ITEMKEYS[fi]] = ''
            else:
                info[ITEMKEYS[fi]] = response.css(filter[fi]).extract_first().strip('\t').strip('\r').strip('\n')

        # info['package'] = info['package'].split('/')[0]

        # info['job_description'] = ' '.join(response.css('div.main-message div.content::text').extract())
        # info['qulification'] = ' '.join(response.css('div.main-message div.content::text').extract())

        info['original_site_name'] = u'智联招聘'
        info['_id'] = response.url
        # a=soup.select(filter['job_decri'])[1]

        return info


    def parse_boss(self, response):
        # resitem = BosssPositionItem()
        for item in response.xpath('//a[@class="lx_job_list mb_15 "]/@href').extract():
            # resitem['posid'] = response.urljoin(item) #.extract()
            # resitem['flag'] = False
            # BosssPositionItem['flag'] = False # not visited yet
            yield scrapy.Request(url=response.urljoin(item), callback=self.parse_boss_pos_info)

    def parse_boss_pos_info(self, response):
        info = PosInfoItem()

        filter = {
            'company': 'div.info-comapny p::text',
            'firm_type': '',
            'firm_detail': '',
            'position': 'div.info-primary div.name a::text',
            'recruit_type': '',
            'publish_time': 'div.info-primary span.time::text',
            'location': 'div.info-primary p::text',
            'package': 'div.info-primary div.name a span::text',
            'job_decri': 'div.detail-content div.job-sec',
            'qualification': '',
            'contact_info': '',
            'original_web': '',
            'URL': '',
        }.values()
        filter = [
            'div.info-comapny p::text',
            '',
            '',
            'div.info-primary div.name a::text',
            '',
            'div.info-primary span.time::text',
            'div.info-primary p::text',
            'div.info-primary div.name a span::text',
            'div.detail-content div.job-sec',
            '',
            '',
            '',
            '',
        ]

        # response.css('div.detail-content div.job-sec').extract_first()
        for fi in range(len(ITEMKEYS)):
            if not filter[fi]:
                info[ITEMKEYS[fi]] = ''
            else:
                info[ITEMKEYS[fi]] = response.css(filter[fi]).extract_first().strip('\t').strip('\r').strip('\n')


        info['job_decri'] = info['job_decri']


        if re.search(r'\d\d月\d\d日', info['publish_time']):
            info['publish_time'] = re.search(r'\d\d月\d\d日', info['publish_time'])

        info['original_site_name'] = u'boss直聘'
        info['_id'] = response.url
        # a=soup.select(filter['job_decri'])[1]

        return info


    # TODO to be reserved
    def parse(self, response):
        resitem = BosssPositionItem()
        for item in response.xpath('//a[@class="lx_job_list mb_15 "]/@href').extract():
            resitem['posid'] = response.urljoin(item)  # .extract()
            resitem['flag'] = False
            # BosssPositionItem['flag'] = False # not visited yet
            yield resitem