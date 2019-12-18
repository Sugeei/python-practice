#!/usr/bin/python
# -*- coding: UTF-8 -*

import scrapy
import os
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from positions.items import PositionsItem,QuotesItem, CnblogsItem
from scrapy.selector import Selector
from positions.timetransformer import transform_timeformat
from settings import USER_AGENTS


class PositionSpider(scrapy.Spider):
    name = "positionspider"
    # allowed_domains = ['liepin.com']
    start_urls = [
        'https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&key=数据&curPage={}'
      ,]

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Host': 'liepin.com',
        'User-Agent': USER_AGENTS[0],
    }

    # 定义爬取URL的规则，并指定回调函数为parse_item
    # rules = [
    #     Rule(LinkExtractor(allow=("/tornadomeet/default.html\?page=\d{1,}")),  # 此处要注意?号的转换，复制过来需要对?号进行转换。
    #          follow=True,
    #          callback='parse_blog')
    # ]
    # print("**********我是博客园爬虫，神奇的分割线**********")

    def start_requests(self):
        return [scrapy.Request(url=self.start_urls[0],
                               headers=self.headers,
                               meta={'cookiejar': 1},
                               callback=self.parse)]

    def parse(self, response):
        # item = PositionsItem() # 实例化item 不能放这里

        for position in response.xpath('//*[@id="sojob"]/div[3]/div/div[1]/div/ul/li'):
            item = PositionsItem()
            # xpath '//*[@id="sojob"]/div[3]/div/div[1]/div/ul'
            item['position_url'] = position.xpath(
                './/div/div[1]/span/a/@href').extract_first()  # '/job_detail/1410591898.html'

            item['position_name'] = position.xpath(
                './/div/div[1]/span/a/text()').extract_first()

            # xpath.extract_first() 返回的是一个NoneType, 如果需要做strip等处理需要先转换成str
            item['position_name'] = str(item['position_name']).strip('\r').strip('\t')

            item['salary'] = position.xpath(
                './/div/div[1]/p[1]/span/text()').extract_first()

            # position.xpath('//*[@id="sojob"]/div[3]/div/div[1]/div[2]/ul/li[1]/div/div[2]/p[1]/a/@href').extract_first()
            item['location'] = position.xpath('.//div/div[1]/p[1]/a/text()').extract_first()
            item['year_experience'] = position.xpath('.//div/div[1]/p[1]/span[3]/text()').extract_first()
            item['degree'] = position.xpath('.//div/div[1]/p[1]/span[2]/text()').extract_first()

            publish_time = position.xpath(
                './/div/div[1]/p[2]/time/text()').extract_first()
            item['publish_time'] = transform_timeformat(str(publish_time))
            '''
            # ERROR
              File "/Users/shujinhuang/positions/positions/spiders/position_spider.py", line 42, in parse
                item['publish_time'] = transform_timeformat(publish_time)
              File "/Users/shujinhuang/positions/positions/timetransformer.py", line 13, in transform_timeformat
                if re.match('\d*-\d*-\d', timestring):
              File "/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/re.py", line 163, in match
                return _compile(pattern, flags).match(string)
            '''

            item['company_name'] = position.xpath(
                './/div/div[2]/p[1]/a/text()').extract_first()

            item['company_url'] = position.xpath('.//div/div[2]/p[1]/a/@href').extract_first()
            item['industry'] = position.xpath(
                './/div/div[2]/p[2]/span/a/text()').extract_first()

            item['original_site_name'] = '猎聘'

            item['_id'] = str(item['position_url']) + str(item['publish_time'])
            '''
            # ERROR
                item['_id'] = item['position_url'] + item['publish_time']
                TypeError: unsupported operand type(s) for +: 'NoneType' and 'NoneType'
            '''

            '''
            公司名称, company_name
            职位名称, position_name
            职位所属部门 department
            公司简介 company_detail
            公司领域 industry
            公司发展阶段 company_level
            公司规模 company_size
            公司主页链接 company_homepage
            工作地点 location
            薪水salary
            经历要求 year_experience
            学历要求 degree
            职位描述 job_description,
            任职要求 qulification
            发布时间 publish_time
            网站名称 original_site_name
            信息来源 position_url
            '''
            yield item

        # next_page = response.css('li.next a::attr(href)').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)


    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()
        yield {
        'name': extract_with_css('h3.author-title::text'), 'birthdate': extract_with_css('.author-born-date::text'), 'bio': extract_with_css('.author-description::text'),
        }


