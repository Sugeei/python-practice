# coding=utf8
import json
import pymssql
# import MySQLdb
import pymysql
import pymongo
from config import logger


class MongoConn(object):
    def __init__(self, mongo_url):
        # mongo_url = "mongodb://app_reportsdb:h8sgk6RjALqKzJm@nosql05.wmcloud-dev.com/reports_db"
        self.mongo_url = mongo_url
        self.mongo_conn = pymongo.MongoClient(mongo_url, connect=False)
        last_slash = mongo_url.rfind('/')
        last_que = mongo_url.rfind('?')
        self.db_name = mongo_url[last_slash + 1:last_que] if last_que > last_slash else mongo_url[last_slash + 1:]

    def connect(self):
        mongo_db = self.mongo_conn.get_database(self.db_name)
        logger.info("mongo connection creation with url = %s" % self.mongo_url)
        return mongo_db


class MysqlConn(object):
    def __init__(self, config_json_str):
        # self.mysql_config = {"host": "db-bigdata.wmcloud-qa.com",  "port": 3312, "db": "bigdata",
        # "user": "app_bigdata_ro", "passwd": "Welcome_20141217"}
        self.mysql_config = json.loads(config_json_str, encoding='utf-8')

    def connect(self):
        mysql_conn = pymysql.connect(**self.mysql_config)
        logger.info("mysql connection creation with config = %s" % self.mysql_config)
        return mysql_conn


class MssqlConn(object):
    def __init__(self, config_json_str):
        # self.mssql_config = {"server": "sh-datayesdb.wmcloud-dev.com",  "port": 1433, "database": "datayesdb",
        #     "user": "talend_load", "password": "Welcome01"}
        self.mssql_config = json.loads(config_json_str, encoding='utf-8')

    def connect(self):
        mssql_conn = pymssql.connect(**self.mssql_config)
        logger.info("mssql connection creation with config = %s" % self.mssql_config)
        return mssql_conn
