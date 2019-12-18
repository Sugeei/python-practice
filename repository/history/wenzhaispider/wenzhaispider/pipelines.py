# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings

#
# MONGODB_HOST = 'localhost' # Change in prod
# MONGODB_PORT = 27017 # Change in prod
# MONGODB_DATABASE = "position" # Change in prod
# MONGODB_POSID = "posid"
# MONGODB_POSINFO = "posinfo"
# MONGODB_USERNAME = "sxy" # Change in prod
# MONGODB_PASSWORD = "sxy"

class MongoPipeline(object):

    collection_name = 'positionid'

    def __init__(self, ):
        connection = pymongo.MongoClient(
            settings['MONGODB_HOST'],
            settings['MONGODB_PORT']
        )

        db = connection[settings['MONGODB_DATABASE']]

        self.collection = db[settings['MONGODB_POSINFO']]
        # self.collection.create_index([('_id', pymongo.DESCENDING)], unique=True)

    def close_spider(self, spider):
        pass
        # self.client.close()

    def process_item(self, item, spider):
        # for data in item:
        #     if not data:
        #         raise DropItem("Missing data!")
        # data = {}
        # data['_id'] = item['posid']
        # data['flag'] = item['flag']
        # dict(item)
        if item:
            self.collection.insert(dict(item))
        # log.msg("News added to MongoDB database!", level=log.DEBUG, spider=spider)
        # return item
        # self.db[self.collection_name].insert(dict(item))
        return item
