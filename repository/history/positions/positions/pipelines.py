# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class PositionsPipeline(object):
    def process_item(self, item, spider):
        return item


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
# from scrapy import log
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
# import MySQLdb
# import MySQLdb.cursors
import pymongo
from scrapy.conf import settings


class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('positions.json', 'w+', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()
#
#
# class MySQLStorePipeline(object):
#     def __init__(self, dbpool):
#         self.dbpool = dbpool
#
#     @classmethod
#     def from_settings(cls, settings):
#         dbargs = dict(
#             host=settings['MYSQL_HOST'],
#             db=settings['MYSQL_DBNAME'],
#             user=settings['MYSQL_USER'],
#             passwd=settings['MYSQL_PASSWD'],
#             charset='utf8',
#             cursorclass=MySQLdb.cursors.DictCursor,
#             use_unicode=True,
#         )
#         dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
#         return cls(dbpool)
#
#     # pipeline默认调用
#     def process_item(self, item, spider):
#         d = self.dbpool.runInteraction(self._do_upinsert, item)
#         # d.addErrback(self._handle_error)
#         return item
#
#     # 将每行更新或写入数据库中
#     def _do_upinsert(self, conn, item):
#         linkmd5id = self._get_linkmd5id(item)
#
#         now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
#         conn.execute("""
#             select 1 from cnblogsinfo where linkmd5id = %s
#             """, (linkmd5id,))
#         ret = conn.fetchone()
#
#         if ret:
#             conn.execute("""
#                 update cnblogsinfo set title = %s, description = %s, link = %s, read_num = %s, comment_num = %s, update_time = %s where linkmd5id = %s
#             """, (item['title'].strip(), item['desc'].strip(), item['link'], item['read_num'], item['comment_num'], now,
#                   linkmd5id))
#             # print """
#             #    update cnblogsinfo set title = %s, description = %s, link = %s, read_num = %s, comment_num = %s, update_time = %s where linkmd5id = %s
#             # """, (item['title'].strip(), item['desc'].strip(), item['link'], item['read_num'], item['comment_num'], now, linkmd5id)
#         else:
#             conn.execute(" \
#             insert into cnblogsinfo(linkmd5id, title, description, link, read_num, comment_num, update_time) \
#             values(%s, %s, %s, %s, %s, %s, %s); \
#             ", (
#             linkmd5id, item['title'].strip(), item['desc'].strip(), item['link'], item['read_num'], item['comment_num'],
#             now))
#             # print "\
#             # insert into cnblogsinfo(linkmd5id, title, description, link, read_num, comment_num, update_time) \
#             # values(%s, %s, %s, %s, %s, %s, %s) \
#             # " ,(linkmd5id, item['title'].strip(), item['desc'].strip(), item['link'], item['read_num'], item['comment_num'], now)
#
#     # 获取url的md5编码
#     def _get_linkmd5id(self, item):
#         # url进行md5处理，为避免重复采集设计
#         return md5(item['link']).hexdigest()
#
#     # 异常处理
#     def _handle_error(self, failue):
#         log.err(failure)
#
#
class MongoStorePipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DATABASE']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    # def close_spider(self, spider):
    #     self.client.close()

    def process_item(self, item, spider):
        for data in item:
            if not data:
                pass
                # raise DropItem("Missing data!")
        try:
            self.collection.insert(dict(item))
        except pymongo.errors.DuplicateKeyError:
            print('duplicate key error :' , item['_id'])
        # log.msg("News added to MongoDB database!", level=log.DEBUG, spider=spider)
        return item
#