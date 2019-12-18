import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from positions.items import PositionsItem

class MySpider(CrawlSpider):

    name = 'lagou'
    allowed_domains = ['zhipin.com']

    urlorigin = 'https://www.zhipin.com/niuren/joblist.html?key={}'
    key = u'数据'.encode('utf-8')
    urlbase = urlorigin.format(key)
    #https://www.zhipin.com/c101020100/h_101020100/?query=数据&page=2&ka=page-2
    start_urls = ['https://www.zhipin.com/c101020100/h_101020100/?query=数据']

    rules = (
    # Extract links matching 'category.php' (but not matching 'subsection.php')
    # and follow links from them (since no callback means follow=True by default). Rule(LinkExtractor(allow=('category\.php', ),
    # deny=('subsection\.php', ))),
    # Extract links matching 'item.php' and parse them with the spider's method parse_item
    #         Rule(
    #             LinkExtractor(allow=('www.zhipin.com/c101020100/h_101020100/\?query=数据&page=\d{1,2}&ka=page-\d{1,2}',)),
    #             callback='parse_position_info'),
            Rule(
                LinkExtractor(allow=('www.zhipin.com/c101020100/h_101020100/\?query=数据&page=\d{1,2}',)),
                callback='parse_position_info'),
        )
    def parse_position_info(self, response):
        # self.logger.info('Hi, this is an item page! %s', response.url)
        # item = scrapy.Item()
        item = PositionsItem()
        # item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)') item['name'] = response.xpath('//td[@id="item_name"]/text()').extract() item['description'] = response.xpath('//td[@id="item_description"]/text()').extract() return item

        print("--------parse page---------")
        for position in response.xpath('//*[@id="main"]/div[3]/div[2]/ul/li'):
            # blog_item = PositionsItem()
            # https://www.zhipin.com/job_detail/1410619098.html
            item['position_url'] = response.urljoin(position.xpath('.//*[@id="main"]/div[3]/div[2]/ul/li[1]/a/@href').extract_first()) # '/job_detail/1410591898.html'

            item['position_name'] = position.xpath('.//*[@id="main"]/div[3]/div[2]/ul/li[1]/a/div[1]/div[1]/h3/text()').extract_first()
            item['salary'] = position.xpath(
                './/*[@id="main"]/div[3]/div[2]/ul/li[1]/a/div[1]/div[1]/h3/span/text()').extract_first()

            detail = position.xpath('.//*[@id="main"]/div[3]/div[2]/ul/li[1]/a/div[1]/div[1]/p/text()').extract()
            # ['上海', '3-5年', '本科']

            item['location'] = detail[0]
            item['year_experience'] = detail[1]
            item['degree'] = detail[2]

            publish_time = position.xpath('.//*[@id="main"]/div[3]/div[2]/ul/li[1]/a/div[3]/span/text()').extract_first()
            item['publish_time'] = publish_time

            item['company_name'] = position.xpath('.//*[@id="main"]/div[3]/div[2]/ul/li[1]/a/div[1]/div[2]/div/h3/text()').extract_first()
            item['company_name'] = position.xpath(
                '//*[@id="main"]/div[3]/div[2]/ul/li[1]/a/div[1]/div[2]/div/h3/text()').extract_first()


            detail = position.xpath('//*[@id="main"]/div[3]/div[2]/ul/li[1]/a/div[1]/div[2]/div/p/text()').extract()
            # ['数据服务', 'A轮', '20-99人']
            item['industry'] = detail[0]
            item['company_level'] = detail[1]
            item['company_size'] = detail[2]

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