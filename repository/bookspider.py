#-*- coding:utf-8 -*-
import scrapy
from douban.items import DoubanBookItem

class BookSpider(scrapy.Spider):
    name='douban-book'
    allowed_domins=['douban.com']
    start_urls=['https://book.douban.com/top250']
    def parse(self,response):
        yield scrapy.Request(response.url,callback=self.parse_next)

        from scrapy.shell import inspect_response
        inspect_response(response, self)  # Rest of parsing code.
        for page in response.xpath('//div[@class="paginator"]/a'):

            link=page.xpath('@herf').extract()[0]
            yield scrapy.Request(link, callback=self.parse_next)
                 
    def parse_next(self,response):
        from scrapy.shell import inspect_response
        inspect_response(response, self)  # Rest of parsing code.

        for item in response.xpath('//tr[@class="item"]'):
            book=DoubanBookItem()
            #初始化读取item列表
            book['name']=item.xpath('td[2]/div[1]/a/@title').extract()[0]
            book['price']=item.xpath('td[2]/p/text()').extract()[0]
            book['ratings']=item.xpath('td[2]/div[2]/span[2]/text()').extract()[0]
            yield book
          