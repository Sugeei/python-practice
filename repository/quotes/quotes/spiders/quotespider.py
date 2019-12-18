# -*- coding: utf-8 -*-
import scrapy


class QuotespiderSpider(scrapy.Spider):
    name = "quotespider"
    allowed_domains = ["quotes.toscrape.com/page/1/"]
    start_urls = ['http://quotes.toscrape.com/page/1//']

    # 爬取主页面, 获得
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
            next_page = response.css('li.next a::attr(href)').extract_first()
            flag = 0
            if next_page is not None and flag < 10 :
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
                flag += 1

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }

