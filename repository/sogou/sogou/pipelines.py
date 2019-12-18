# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy import log

#
# class MongoDBPipeline(object):
#     def __init__(self):
#         connection = pymongo.MongoClient(
#             settings['MONGODB_SERVER'],
#             settings['MONGODB_PORT']
#         )
#         db = connection[settings['MONGODB_DATABASE']]
#         self.collection = db[settings['MONGODB_COLLECTION']]
#
#     def process_item(self, item, spider):
#         if item['title']:
#             item['title'] = wash(item['title'])
#         if item['brief_text']:
#             item['brief_text'] = wash(item['brief_text'])
#         if item['author']:
#             item['author'] = wash(item['author'])
#         if item['time']:
#             item['time'] = wash(item['time'])
#         for data in item:
#             if not data:
#                 raise DropItem("Missing data!")
#         self.collection.insert(dict(item))
#         log.msg("Question added to MongoDB database!",
#                 level=log.DEBUG, spider=spider)
#         return item

class QuaPipeline(object):
    def process_item(self, item, spider):
        return item