# -*- coding: utf-8 -*-
import scrapy


class PositionspiderSpider(scrapy.Spider):
    name = "positionspider"
    allowed_domains = ["www.liepin.com"]
    start_urls = ['http://www.liepin.com/']

    def parse(self, response):
        pass
