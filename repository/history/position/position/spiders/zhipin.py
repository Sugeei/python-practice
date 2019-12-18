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
from position.settings import KEY as keys
# Below two lines are used for debugging
from scrapy.shell import inspect_response
# inspect_response(response, self)  # Rest of parsing code.

import time
import random

### 一定要研究清楚目标站点的结构!
### 一定要研究清楚目标站点的结构!
### 一定要研究清楚目标站点的结构!
'''
https://www.zhipin.com/job_detail/?query=%E6%95%B0%E6%8D%AE&scity=101280100&source=2&page=3
scity is city id
'''
# 广州, 北京, 上海, 深圳, 杭州
cityid = ['101280100','101010100','101020100','101280600','101210100']
cityid = ['101020100']

class ZhipinSpider(scrapy.Spider):

    name = "zhipin"
    allowed_domains = ["zhipin.com"]

    # start_urls = ['https://www.liepin.com/zhaopin']
    start_url = 'https://www.zhipin.com/job_detail/?query={}&scity={}&source=2'
    start_urls = []  #'https://www.liepin.com/zhaopin/?key=数据'
    for key in keys:
        for city in cityid:
            start_urls.append(start_url.format(key, city))

    # def parse_anti_spider(self, response):
    #     # 如果有验证码要人为处理
    #     # https://www.zhipin.com/captcha/popUpCaptcha?redirect=https%3A%2F%2Fwww.zhipin.com%2Fjob_detail%2F%3Fquery%3D%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD%26scity%3D101020100%26source%3D2%26page%3D24
    #     if 'id="captcha"' in response.body:
    #         link = response.xpath('//div[@class="capcha-box"]/form/p/img/@src').extract()[0]
    #         link = response.urljoin(response.xpath('//div[@class="capcha-box"]/form/p/img/@src').extract()[0])
    #         print('There is something you need to deal with: ', link)
    #
    #         captcha_solution = input('Input captcha-solution: ')
    #         captcha_id = response.xpath('//input[@id="captcha"]')
    #         # urlparse.parse_qs(urlparse.urlparse(link).query, True)['id']
    #         self.formdata['captcha-solution'] = captcha_solution
    #         self.formdata['captcha-id'] = captcha_id
    #         return [scrapy.FormRequest.from_response(response,
    #                                              formdata=self.formdata,
    #                                              headers=self.headers,
    #                                              meta={'cookiejar': response.meta['cookiejar']},
    #                                              callback=self.after_login
    #                                              )]

    def parse(self, response):
        # //*[@id="sojob"]/div[2]/div/div[1]/div/ul
        ### xpath 建议自己写, chrome 给出的做参考, 多用'//'而不是'/', 会对路径变化的适应力较强
        # //*[@id="main"]/div[3]/div[2]
        for position in response.xpath('//div[@class="job-list"]/ul/li'):
            item = PositionItem()
            #
            # html 修改前 //*[@id="sojob"]/div[2]/div/div[1]/div/ul/li[1]/div/div[1]/h3/a
            # xpath .//div/div[1]/h3/a
            # html 修改后 //*[@id="sojob"]/div[3]/div/div[1]/div[2]/ul/li[40]/div/div[1]/span/a
            # xpath .//div//a
            item['position_url'] = response.urljoin(position.xpath('.//a/@href').extract_first())  # '/job_detail/1410591898.html'
            #//*[@id="sojob"]/div[2]/div/div[1]/div/ul/li[1]/div/div[1]/h3/a
            # jobinfo = position.xpath('.//div[@class="job-info"]')
            # //*[@id="main"]/div[3]/div[2]/ul/li[1]/a/div[1]/div[1]/h3 class="info-primary"
            position_name = position.xpath('.//div[@class="info-primary"]//h3/text()').extract_first()

            item['position_name'] = ''.join(str(position_name).split()) # 去掉所有空白字符

            # xpath.extract_first() 返回的是一个NoneType, 如果需要做strip等处理需要先转换成str

            item['salary'] = position.xpath('.//div[@class="info-primary"]//h3/span/text()').extract_first()

            # position.xpath('//*[@id="sojob"]/div[3]/div/div[1]/div[2]/ul/li[1]/div/div[2]/p[1]/a/@href').extract_first()
            detail = position.xpath('.//div[@class="info-primary"]/p/text()').extract()
            ### ['广州', '1-3年', '大专']
            '''
            for a structure like below, for item in xpath[@class="whatever"]
            why xpath('.//div[@class="info-primary"]//p/text()').extract() get all <div class="info-primary"> ???
            <div class="whatever">
                <div class="info-primary">
                    <p>
                        beijin
                        <em></em>
                        3 years
                        <em></em>
                </div>
            </div>
            <div>
                <div class="info-primary">
                    <p>
                        shanghai
                        <em></em>
                        3 years
                        <em></em>
                </div>
            </div>
            '''
            item['location'] = detail[0]
            item['year_experience'] = detail[1]
            item['degree'] = detail[2]

            # //*[@id="main"]/div[3]/div[2]/ul/li[1]/a/div[3]/span
            publish_time = position.xpath('.//div[@class="job-time"]/span/text()').extract_first()

            item['publish_time'] = transform_timeformat(str(publish_time))

            item['company_name'] = position.xpath(
                './/div[@class="company-text"]/h3/text()').extract_first()

            detail = position.xpath(
                './/div[@class="company-text"]/p/text()').extract() # extract 提取出来的是一个列表
            # ['数据服务', 'A轮', '100-499人']

            # item['company_url'] = position.xpath('.//div/div[2]/p[1]/a/@href').extract_first()
            try:
                item['industry'] = detail[0]
                item['company_level'] = detail[1]
                item['company_size'] = detail[2]
            except:
                pass

            # class="job-tags"
            detail = position.xpath('.//div[@class="job-tags"]/span/text()').extract()
            item['job_description'] = ','.join(detail)

            item['original_site_name'] = 'Boss直聘' #u'猎聘'.encode('utf-8')

            item['_id'] = str(item['position_url']) + str(item['publish_time'])

            item['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['crawldetailflag'] = False
            yield item

        # 取出当前页的id,
        #'//*[@id="sojob"]/div[2]/div/div[1]/div/div/div
        #'//*[@id="sojob"]/div[2]/div/div[1]/div/div/div/a[5]'
        curr_page_id = response.xpath('//div[@class="page"]//a[@class="cur"]/text()').extract_first()
        # curr_page_id = response.xpath('//*[@id="sojob"]/div/div/div[1]/div/div/div/a[@class="current"]/text()').extract_first()

        # TODO to deal with anti-anti-spider
        # <h1 class="warning-msg">系统检测到您账号的操作行为过于频繁，请确认是本人操作，同时不要将账号信息透漏给其人或其它软件，尽量不要和其他人共用账号，如有以上行为请立即修改密码。</h1>
        # <div class="tips">为了您的账号安全，我们需要在执行操作之前验证您的身份，请输入验证码。
        warningmsg = response.xpath('//*[@class="warning-msg"]').extract_first()
        if warningmsg:
            pass

        # TODO get next page
        ### 爬虫的停止条件需要研究目标页面的结构
        # <a class="disable">下一页</a>
        # 当不是最后一页时,next_page为空, 正好是我所需要的, 用它判断是否还是下一页需要爬取
        next_page_disable = response.xpath('//a[@ka="page-next"][contains(@class, "disabled")]').extract_first()
        # next_page_disable = response.xpath('//a[@ka="page-prev"][contains(@class, "disabled")]').extract_first()
        # next_page = response.xpath('//*[@id="sojob"]/div[3]/div/div[1]/div[2]/div/div/a[text()="下一页"]/text()').extract_first()
        # inspect_response(response, self)  # Rest of parsing code.
        if next_page_disable is None and int(curr_page_id) < 10:

            for key in keys:
                for city in cityid:
                    url = 'https://www.zhipin.com/job_detail/?query={}&scity={}&source=2&page={}'.format(key, city, str(int(curr_page_id)+1))
                    randomsleep = random.randint(10,30)
                    time.sleep(randomsleep)
                    # inspect_response(response, self)  # Rest of parsing code.
                    yield scrapy.Request(url, callback=self.parse) #,
                    #                          headers=headers, )

                    ### 傻了我, 根本不需要多么花哨的headers, 也不需要去页面中找下一页链接, 直接在url中改页码id即可, 然后发送请求
                    ### 小心翼翼,尽量不给服务器太大压力,(不让服务器发现我)


