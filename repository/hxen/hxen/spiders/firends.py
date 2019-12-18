# -*- coding: utf-8 -*-
import scrapy


class FirendsSpider(scrapy.Spider):
    name = "firends"
    allowed_domains = ["hxen.com"]
    start_urls = ['http://hxen.com/']

    #
    def parse(self, response):
        for url in response.xpath('//*[@id="news"]/div/div/div/div/em/a/@href'):
            full_url = response.urljoin(url.extract())
            yield scrapy.Request(full_url, self.parse_page)

        next_page = response.css('li.next a::attr(href)').extract_first()

        # get paginator next page
        if next_page is not None :
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    #
        for rowValue in response.xpath('//table/tr'):
            row = rowValue.xpath('//tb').extract()
            if row:
                print()

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }


