# -*- coding: utf-8 -*-
import scrapy



class LiepindailySpider(scrapy.Spider):
    name = "liepindaily"
    allowed_domains = ["liepin.com"]
    start_urls = ['http://liepin.com/']

    def parse(self, response):
        pass
