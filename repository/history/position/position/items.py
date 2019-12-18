# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


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
专业要求 majorwanted
经历要求 year_experience
学历要求 degree
职位描述 job_description,
任职要求 qulification
发布时间 publish_time
网站名称 original_site_name
信息来源 position_url
'''

ITEMKEYS = [
    'company_name',
    'company_type',
    'company_detail',
    'position_name',
    'position_type',
    'majorwanted',
    'publish_time',
    'location',
    'salary',
    'job_description',
    'qulification',
    'recuitnumber',
    'original_site_name',
    '_id',
    'department',
    'industry',
    'company_level',
    'company_url',
    'company_size',
    'company_homepage',
    'year_experience',
    'degree',
    'position_url'

]

class PositionItem(scrapy.Item):
    # define the fields for your item here like:
    # get below info from position list website

    ITEMKEYS = [
        'company_name',
        'company_type',
        'company_detail',
        'position_name',
        'position_type',
        'majorwanted',
        'publish_time',
        'location',
        'salary',
        'job_description',
        'qualification',
        'recuitnumber',
        'original_site_name',
        '_id',
        'department',
        'industry',
        'company_level',
        'company_url',
        'company_size',
        'company_homepage',
        'year_experience',
        'degree',
        'position_url'

    ]
    company_name = scrapy.Field()
    company_type = scrapy.Field()
    company_detail = scrapy.Field()
    position_name = scrapy.Field()
    position_type = scrapy.Field()
    publish_time = scrapy.Field()
    location = scrapy.Field()
    salary = scrapy.Field()
    job_description = scrapy.Field()
    qulification = scrapy.Field()

    original_site_name = scrapy.Field()

    _id = scrapy.Field()
    department = scrapy.Field()
    industry = scrapy.Field()
    company_level = scrapy.Field()
    company_url = scrapy.Field()
    company_size = scrapy.Field()
    company_homepage = scrapy.Field()
    year_experience = scrapy.Field()
    degree = scrapy.Field()
    position_url = scrapy.Field()

    timestamp = scrapy.Field()
    #
    crawldetailflag = scrapy.Field() #默认值为false, 表示不爬取当前职位的详情页面, 为True表示需要爬取此职位的详情页面获取相关信息

    pass
