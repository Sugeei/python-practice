# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BosssPositionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    posid = scrapy.Field()
    flag = scrapy.Field()
    pass


ITEMKEYS = [
    'company_name',
    'company_type',
    'company_detail',
    'position_name',
    'position_type',
    'publish_time',
    'location',
    'package',
    'job_description',
    'qulification',
    'contact_info',
    'original_site_name',
    '_id'
]



class PosInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    company_name = scrapy.Field()
    company_type = scrapy.Field()
    company_detail = scrapy.Field()
    position_name = scrapy.Field()
    position_type = scrapy.Field()
    publish_time = scrapy.Field()
    location = scrapy.Field()
    package = scrapy.Field()
    job_description = scrapy.Field()
    qulification = scrapy.Field()
    contact_info = scrapy.Field()
    original_site_name = scrapy.Field()
    _id = scrapy.Field()


class BossPosInfoItem(PosInfoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # self.selector = {
    #     'company': 'div.info-comapny p',
    #     'firm_type': '',
    #     'firm_detail': '',
    #     'position': 'div.info-primary div.name a',
    #     'recruit_type': '',
    #     'publish_time': 'div.info-primary span.time',
    #     'location': 'div.c_property p.info',
    #     'package': 'div.info-primary div.name a span',
    #     'job_decri': 'div.job-desc_container p',
    #     'qualification': '',
    #     'contact_info': '',
    #     'original_web': '',
    #     'URL': '',
    # }
    pass

