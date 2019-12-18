import scrapy
import os
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from positions.items import PositionsItem,QuotesItem, CnblogsItem
from scrapy.selector import Selector

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',]
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
                }
        # next_page = response.css('li.next a::attr(href)').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)


    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()
        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }


# class QuotesSpider2(scrapy.Spider):
#     name = "quotes"
#     start_urls = [
#         'http://quotes.toscrape.com/tag/humor/',
#     ]
#
#     def parse(self, response):
#         for quote in response.css('div.quote'):
#             yield {
#                 'text': quote.css('span.text::text').extract_first(),
#                 'author': quote.xpath('span/small/text()').extract_first(),
#             }
#
#         next_page = response.css('li.next a::attr("href")').extract_first()
#         if next_page is not None:
#             next_page = response.urljoin(next_page)
#             yield scrapy.Request(next_page, callback=self.parse)