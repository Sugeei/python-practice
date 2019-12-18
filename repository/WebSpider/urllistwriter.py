#!usr/bin/env python
#_*_ coding: utf-8 _*_
#
#  :param  list of position's url
#  this is the first process of the spider
#  insert url into database


class UrlListWriter():
    def __init__(self, postion_url_list, db_table):
        self.url_list = postion_url_list
        self.table = db_table
    #
    def write_url_to_db(self):
        pass
