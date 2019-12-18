import scrapy
import pymongo
import re
from wenzhaispider.items import ITEMKEYS, BosssPositionItem, PosInfoItem
from scrapy.conf import settings



class PositionIdSpider(scrapy.Spider):
    name = "bosszhipin"

    def start_requests(self):
        urlorigin = 'https://www.bosszhipin.com/niuren/joblist.html?key={}'
        key = u'数据'
        urlbase = urlorigin.format(key)

        urls = [
                urlbase
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        resitem = BosssPositionItem()
        for item in response.xpath('//a[@class="lx_job_list mb_15 "]/@href').extract():
            resitem['posid'] = response.urljoin(item) #.extract()
            resitem['flag'] = False
            # BosssPositionItem['flag'] = False # not visited yet
            yield resitem
        # return response.xpath('//a[@class="lx_job_list mb_15 "]/@href').extract()

    #
    # def parse(self, response):
    #     page = response.url.split("/")[-2]
    #     filename = 'quotes-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log('Saved file %s' % filename)

class PositionInfoSpider(scrapy.Spider):
    name = ""

    def start_requests(self):
        # boss zhipin
        urlt = 'https://www.bosszhipin.com/niuren/joblist.html?key={}'
        pos = u'数据'
        url = urlt.format(pos)
        yield scrapy.Request(url=url, callback=self.parse_boss)


        connection = pymongo.MongoClient(
            settings['MONGODB_HOST'],
            settings['MONGODB_PORT']
        )

        db = connection[settings['MONGODB_DATABASE']]
        connection = db[settings['MONGODB_POSID']]
        urls = connection.find({'flag': False})

        # for url in urls[0:2]:
        #     yield scrapy.Request(url=url, callback=self.parse_boss)

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
                info[ITEMKEYS[fi]] = response.css(filter[fi]).extract_first()


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