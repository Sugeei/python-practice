# -*- coding: utf-8 -*-
import scrapy
import os, re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
# from settings import USER_AGENTS
from position.items import PositionItem
from position.timetransformer import transform_timeformat
from datetime import datetime

# Below two lines are used for debugging
from scrapy.shell import inspect_response
# inspect_response(response, self)  # Rest of parsing code.


keys = ['数据']
# keys = ['数据', '机器学习', '人工智能']
class LiepinSpider(scrapy.Spider):

    name = "liepin"
    allowed_domains = ["liepin.com"]

    start_url = 'https://www.liepin.com/zhaopin'

    curpage = 0
    # start_urls = ['https://www.liepin.com/zhaopin']
    start_url = 'https://www.liepin.com/zhaopin/?&sfrom=click-pc_homepage-centre_searchbox-search_new&key={}'
    start_urls = []  #'https://www.liepin.com/zhaopin/?key=数据'
    for key in keys:
        start_urls.append(start_url.format(key))
    # def start_requests(self):
    #
    #     for key in keys:
    #         # 通过分析浏览器request的数据伪造此headers
    #         headers = {
    #             # 'sfrom': 'click-pc_homepage-centre_searchbox-search_new', #click - pc_homepage - centre_searchbox - search_new
    #             'key': key
    #         }
    #         # for url in self.start_urls:
    #         yield scrapy.Request(self.start_url, callback=self.parse,
    #                              headers=headers,)
    #                              #errback=self.errback_httpbin,
    #                              # dont_filter=True)

    def parse(self, response):
        # //*[@id="sojob"]/div[2]/div/div[1]/div/ul
        ### xpath 建议自己写, chrome 给出的做参考, 会对路径的变化适应力较强
        #
        for position in response.xpath('//div[@class="sojob-result "]/ul/li'):
            item = PositionItem()
            #
            # html 修改前 //*[@id="sojob"]/div[2]/div/div[1]/div/ul/li[1]/div/div[1]/h3/a
            # xpath .//div/div[1]/h3/a
            # html 修改后 //*[@id="sojob"]/div[3]/div/div[1]/div[2]/ul/li[40]/div/div[1]/span/a
            # xpath .//div//a
            item['position_url'] = position.xpath('.//div//a/@href').extract_first()  # '/job_detail/1410591898.html'
            #//*[@id="sojob"]/div[2]/div/div[1]/div/ul/li[1]/div/div[1]/h3/a
            # jobinfo = position.xpath('.//div[@class="job-info"]')

            position_name = position.xpath('.//div//a/text()').extract_first()

            item['position_name'] = ''.join(str(position_name).split()) # 去掉所有空白字符

            # xpath.extract_first() 返回的是一个NoneType, 如果需要做strip等处理需要先转换成str

            item['salary'] = position.xpath(
                './/div/div[1]/p[1]/span/text()').extract_first()

            # position.xpath('//*[@id="sojob"]/div[3]/div/div[1]/div[2]/ul/li[1]/div/div[2]/p[1]/a/@href').extract_first()
            item['location'] = position.xpath('.//div/div[1]/p[1]/a/text()').extract_first()
            item['year_experience'] = position.xpath('.//div/div[1]/p[1]/span[3]/text()').extract_first()
            item['degree'] = position.xpath('.//div/div[1]/p[1]/span[2]/text()').extract_first()

            publish_time = position.xpath(
                './/div/div[1]/p[2]/time/text()').extract_first()
            item['publish_time'] = transform_timeformat(str(publish_time))

            item['company_name'] = position.xpath(
                './/div/div[2]/p[1]/a/text()').extract_first()

            item['company_url'] = position.xpath('.//div/div[2]/p[1]/a/@href').extract_first()
            item['industry'] = position.xpath(
                './/div/div[2]/p[2]/span/a/text()').extract_first()

            item['original_site_name'] = '猎聘' #u'猎聘'.encode('utf-8')

            item['_id'] = str(item['position_url']) + str(item['publish_time'])

            item['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['crawldetailflag'] = False
            yield item

        # 取出当前页的id,
        #'//*[@id="sojob"]/div[2]/div/div[1]/div/div/div
        #'//*[@id="sojob"]/div[2]/div/div[1]/div/div/div/a[5]'
        curr_page_id = response.xpath('//div[@class="pagerbar"]//a[@class="current"]/text()').extract_first()
        # curr_page_id = response.xpath('//*[@id="sojob"]/div/div/div[1]/div/div/div/a[@class="current"]/text()').extract_first()
        # TODO to deal with anti-anti-spider
        # <h1 class="warning-msg">系统检测到您账号的操作行为过于频繁，请确认是本人操作，同时不要将账号信息透漏给其人或其它软件，尽量不要和其他人共用账号，如有以上行为请立即修改密码。</h1>
        warningmsg = response.xpath('//*[@class="warning-msg"]').extract_first()
        if warningmsg:
            pass

        # TODO get next page
        ### 爬虫的停止条件需要研究目标页面的结构
        # <a class="disable">下一页</a>
        # 当不是最后一页时,next_page为空, 正好是我所需要的, 用它判断是否还是下一页需要爬取
        next_page_disable = response.xpath('//div[@class="pagerbar"]//a[text()="下一页"]/@class').extract_first()
        # next_page = response.xpath('//*[@id="sojob"]/div[3]/div/div[1]/div[2]/div/div/a[text()="下一页"]/text()').extract_first()
        # inspect_response(response, self)  # Rest of parsing code.
        if next_page_disable is None:
            # url = 'https://www.liepin.com/zhaopin/?&fromSearchBtn=2&init=-1&sfrom=click-pc_homepage-centre_searchbox-search_new&key=%E6%95%B0%E6%8D%AE&curPage=2'
            # self.curpage += 1
            # https://www.liepin.com/zhaopin/?fromSearchBtn=2&init=-1&key=java&curPage=2
            for key in keys:
                url = 'https://www.liepin.com/zhaopin/?fromSearchBtn=2&init=-1&key={}&curPage={}'.format(key, str(int(curr_page_id)+1))
                # for key in keys:
                #     # 通过分析浏览器request的数据伪造此headers
                #     headers = {
                #         'fromSearchBtn': 2
                #         'init': -1,
                #         # 'sfrom': 'click-pc_homepage-centre_searchbox-search_new',
                #         'key': key,
                #         'curPage':  str(self.curpage),
                #     }
                # inspect_response(response, self)  # Rest of parsing code.
                yield scrapy.Request(url, callback=self.parse) #,
                #                          headers=headers, )

        ### 傻了我, 根本不需要多么花哨的headers, 也不需要去页面中找下一页链接, 直接在url中改页码id即可, 然后发送请求
        ### 小心翼翼,尽量不给服务器太大压力,(不让服务器发现我)


