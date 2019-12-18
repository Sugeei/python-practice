import scrapy
import os
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from positions.items import PositionsItem,QuotesItem, CnblogsItem
from scrapy.selector import Selector


class QuotesSpider(CrawlSpider):
    name = "test"

    allowed_domains = ['cnblogs.com']
    start_urls = [
        "http://www.cnblogs.com/tornadomeet/default.html?page=1"
    ]
    rules = [Rule(LinkExtractor(allow=("/tornadomeet/default.html\?page=\d{1,2}")),  # 此处要注意?号的转换，复制过来需要对?号进行转换。
             follow=True,
             callback='parse_blog')
    ]

    def parse_blog(self, response):
        print("--------解析目录页面---------")
        for blog in response.xpath('//div[@class="day"]'):
            blog_item = CnblogsItem()
            blog_item['title'] = blog.xpath('.//div[@class="postTitle"]/a/text()').extract_first()
            blog_item['link'] = response.urljoin(blog.xpath('.//div[@class="postTitle"]/a/@href').extract_first())
            blog_item['desc'] = blog.xpath('.//div[@class="c_b_p_desc"]/text()').extract_first()
            blog_info = blog.xpath('.//div[@class="postDesc"]/text()').extract_first()
            blog_item['read_num'] = blog_info.split('(')[1].split(')')[0]
            blog_item['comment_num'] = blog_info.split('(')[2].split(')')[0]

            yield blog_item

    def parse_url(self, response):
        selector = Selector(response)
        item = QuotesItem()

        # print "parse_item>>>>>>"

        # blog_url = str(response.url)
        author = selector.xpath('/html/body/div/div[2]/div[1]/div[1]/span[2]/a/@href').extract()
        item['title'] = response.url

        yield item
        # self.logger.info('Hi, this is an item page! %s', response.url)

'''
scrapy shell http://quotes.toscrape.com/page/1/

In [7]: response.xpath('/html/body/div/div[2]/div[1]/div[1]/span[2]/a/@href').extract()
Out[7]: ['/author/Albert-Einstein']
'''