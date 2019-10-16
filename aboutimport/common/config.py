#! usr/bin/python
# coding=utf-8

from logging import config
import json
import logging
import os
import re
import sys
# from logging import config

import pymssql
import pymysql
# import MySQLdb
import pika
import pymongo
# import yaml
from common.logger import logger

'''Environment variables:
    DYDB
    KAFKA
    MONGO
    SCHEMA_REGISTRY
    RP_MQ
    LOG_LEVEL (optional)
    RP_MACRO_EXCHANGE (optional)
'''

this_dir = os.path.dirname(os.path.realpath(__file__))
base_dir = os.path.dirname(this_dir)

if not os.path.exists(base_dir + "/logs"):
    os.mkdir(base_dir + "/logs")


# with open(this_dir + "/logging.yaml") as f:
#     ycfg = yaml.load(f)
#     ycfg.setdefault('version', 1)
#     logging.config.dictConfig(ycfg)
#
# main_module = sys.modules['__main__'].__file__
# module_dir = os.path.dirname(main_module)
# logger_name = module_dir[module_dir.rfind('/') + 1:]
# # print "main module is %s, logger name is %s" % (main_module, logger_name)
# # logger = logging.basicConfig(filename='fundtags.logs', level=logging.WARNING)
# # print "main module is %s, logger name is %s" % (main_module, logger_name)
# logger = logging.getLogger(logger_name)


class Config:
    def __init__(self):
        """

            DY_DB_RO (datayes db, read only)
                dev  the same
                stg  the same
                prd  {"server":"sh-datamall-db03.datayes.com","port":1433,
                "database":"datayesdb","user":"talend_load",
                "password":"s9t5gNThn2vqWM7c","charset":"utf8"}
            DY_DB_RW  (datayes db)
                dev  {"server":"10.24.21.202","port":1433,
                "database":"datayesdb","user":"talend_load",
                "password":"Welcome01","charset":"utf8"}
                stg  {"server":"db-mssql02.datayes-stg.com","port":1433,
                "database":"datayesdb","user":"talend_load",
                "password":"s9t5gNThn2vqWM7c","charset":"utf8"}
                prd  {"server":"sh-datamall-db03.datayes.com","port":1433,
                "database":"datayesdb","user":"talend_load",
                "password":"s9t5gNThn2vqWM7c","charset":"utf8"}
        """
        self.mssql_db = MssqlConn(os.environ['DY_DB_RW']) if 'DY_DB_RW' in os.environ else None
        self.datayesdb_rw = MssqlConn(os.environ['DY_DB_RW']) if 'DY_DB_RW' in os.environ else None
        #                              """{"server": "10.24.21.202", "port": 1433,
        # "database": "datayesdb", "user": "talend_load",
        # # "password": "Welcome01", "charset": "utf8"}""")

        # read only
        self.datayesdb_ro = MssqlConn(os.environ['DATAYES_DB_RO'] \
                                          if 'DATAYES_DB_RO' in os.environ else """{"server":"sh-datamall-db03.datayes.com","port":1433,
                "database":"datayesdb","user":"talend_load",
                "password":"s9t5gNThn2vqWM7c","charset":"utf8"}""")

        self.mongo = MongoConn(os.environ['MONGO']) if 'MONGO' in os.environ else None
        # 'mongodb://app_dataifs_rw:uaTQIDzoq28o3gf4n@nosql06.wmcloud-dev.com:27017/dataifs')

        self.ashare_mssql_db = MssqlConn(os.environ['ASHARE_DB_RO']) if 'ASHARE_DB_RO' in os.environ else None


    def add_cdc_table(self, database, table, status):
        self.mongo.mongo_db.cdc_tables.find_one_and_update(filter={"database": database, "table": table},
                                                           update={"$set": {"status": status}},
                                                           upsert=True)
        logger.info("add/update cdc table: %s %s" % (database, table))

    def turn_on_cdc_table(self, database, table):
        self.mongo.mongo_db.cdc_tables.find_one_and_update(filter={"database": database, "table": table},
                                                           update={"$set": {"status": "on"}},
                                                           upsert=True)
        logger.info("turn on cdc table: %s %s" % (database, table))

    def get_call_cdc_tables(self):
        docs = self.mongo.mongo_db.cdc_tables.find(filter={"status": "on"})
        ret = []
        for doc in docs:
            ret.append((doc['database'], doc['table']))
        logger.info("got all monitored cdc tables: {0}".format(ret))
        return ret

    def lp_for_cdc_table(self, database, table):
        doc = self.mongo.mongo_db.cdc_tables.find_one(filter={"database": database, "table": table})
        return doc['lp'] if doc is not None and 'lp' in doc else None

    def set_cdc_table_lp(self, database, table, lp):
        self.mongo.mongo_db.cdc_tables.find_one_and_update(filter={"database": database, "table": table},
                                                           update={"$set": {"lp": lp}})


class MongoConn(object):
    def __init__(self, mongo_url):
        # mongo_url = "mongodb://app_reportsdb:h8sgk6RjALqKzJm@nosql05.wmcloud-dev.com/reports_db"
        mongo_conn = pymongo.MongoClient(mongo_url, connect=False)
        last_slash = mongo_url.rfind('/')
        last_que = mongo_url.rfind('?')
        db_name = mongo_url[last_slash + 1:last_que] if last_que > last_slash else mongo_url[last_slash + 1:]
        self.mongo_db = mongo_conn.get_database(db_name)
        logger.info("mongo connection creation with url = %s" % mongo_url)


class MysqlConn(object):
    def __init__(self, config_json_str):
        # self.mysql_config = {"host": "10.22.128.150",  "port": 3317, "db": "bigdata", "user": "talend_load",
        #   "passwd": "s9t5gNThn2vqWM7c" , "charset" : "utf8"}
        # self.mysql_config = {"host": "db-bigdata.wmcloud-qa.com",  "port": 3312, "db": "bigdata", "user": "app_bigdata_ro",
        #   "passwd": "Welcome_20141217"}
        self.mysql_config = json.loads(config_json_str, encoding='utf-8')

    def connect(self):
        mysql_conn = pymysql.connect(**self.mysql_config)  # pymysql
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

    def __str__(self):
        return json.dumps(self.mssql_config, ensure_ascii=False, encoding='utf-8')


class MqConn(object):
    def __init__(self, mq_url):
        mq_url = mq_url.strip()
        # format: username:password@host:port/virtual_host
        m = re.match(r"(?P<username>.+):(?P<password>.+)@(?P<host>.+):(?P<port>\d+)/?(?P<virtual_host>.*)", mq_url)
        self.mq = {"host": m.group("host"), "port": int(m.group("port")), "username": m.group("username"),
                   "password": m.group("password"), "virtual_host": m.group("virtual_host")}
        self.virtual_host = None if (self.mq['virtual_host'] is None or len(self.mq['virtual_host']) == 0) \
            else self.mq['virtual_host']
        self.channel = None

    def connect(self):
        logging.info(u"trying to connect mq with configuration %s" % self.__str__())
        rp_mq = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.mq['host'], port=self.mq['port'], virtual_host=self.virtual_host,
                                      credentials=pika.PlainCredentials(self.mq['username'], self.mq['password'])))
        self.channel = rp_mq.channel()
        return self.channel

    def __str__(self):
        return json.dumps(self.mq, ensure_ascii=False, encoding='utf-8')


class Debug(object):
    def __init__(self):
        self.this_dir = os.path.dirname(os.path.realpath(__file__))
        self.base_dir = os.path.dirname(self.this_dir)

    def get_debug_status(self):
        debugfile = os.path.join(self.base_dir, 'debug.txt')

        if os.path.exists(debugfile):
            return True
        else:
            return False


#
DEBUG = Debug().get_debug_status()

if __name__ == "__main__":
    cfg = Config()
    conn = cfg.dymysql_db.connect()
    sql = """SELECT a.id AS outKey,
    TICKER_SYMBOL,
    ACT_PUBTIME,
    DATE_FORMAT(ACT_PUBTIME,'%Y-%m-%d') AS TRADE_DATE,
    DATE_FORMAT(end_date,'%Y') AS  END_YEAR,
    EXPN_INCAP_LL AS INCOME_LL,
    EXPN_INCAP_UPL AS INCOME_UPL,
    DATE_FORMAT(a.CREATE_TIME,'%Y-%m-%d %H:%i:%s') AS CREATE_TIME ,
    DATE_FORMAT(a.UPDATE_TIME,'%Y-%m-%d %H:%i:%s') AS UPDATE_TIME
    FROM fdmt_ef a, datayesdb.sys_code b
    WHERE FISCAL_PERIOD = 12 AND PUBLISH_DATE >= '2010-01-01' AND a.FORECAST_TYPE = b.VALUE_NUM_CD AND b.CODE_TYPE_ID=70006
    AND (
    EXPN_INCAP_LL IS NOT NULL AND  EXPN_INCAP_UPL IS NOT NULL
    )
    UNION
    SELECT
    aa.outKey,
    aa.TICKER_SYMBOL,
    aa.ACT_PUBTIME,
    DATE_FORMAT(aa.TRADE_DATE,'%Y-%m-%d') AS TRADE_DATE,
    DATE_FORMAT(aa.END_DATE,'%Y') AS  END_YEAR,
    CASE WHEN aa.INCOME_LL IS NULL THEN
    bb.INCOME_LAST_YEAR*(1+aa.GROWTH_LL/100)
    ELSE aa.INCOME_LL END  AS INCOME_LL,
    CASE WHEN aa.INCOME_UPL IS NULL THEN
    bb.INCOME_LAST_YEAR*(1+aa.GROWTH_UPL/100)
    ELSE aa.INCOME_UPL END AS INCOME_UPL ,
    CREATE_TIME,
    UPDATE_TIME
    FROM
    (
    SELECT a.id AS outKey,
    TICKER_SYMBOL, ACT_PUBTIME, CAST(DATE(ACT_PUBTIME) AS DATETIME) AS TRADE_DATE, CAST(END_DATE AS DATETIME) AS END_DATE,
    N_INCAP_CHGR_LL AS GROWTH_LL,
    N_INCAP_CHGR_UPL AS GROWTH_UPL,
    EXPN_INCAP_LL AS INCOME_LL,
    EXPN_INCAP_UPL AS INCOME_UPL,
    DATE_FORMAT(a.CREATE_TIME,'%Y-%m-%d %H:%i:%s') AS CREATE_TIME ,
    DATE_FORMAT(a.UPDATE_TIME,'%Y-%m-%d %H:%i:%s') AS UPDATE_TIME
    FROM fdmt_ef a, datayesdb.sys_code b
    WHERE FISCAL_PERIOD = 12 AND PUBLISH_DATE >= '2010-01-01' AND a.FORECAST_TYPE = b.VALUE_NUM_CD AND b.CODE_TYPE_ID=70006
    AND
    (
    ((N_INCAP_CHGR_LL IS NOT  NULL  AND  EXPN_INCAP_LL IS  NULL )
    AND(N_INCAP_CHGR_UPL IS NOT NULL AND EXPN_INCAP_UPL IS  NULL))
    OR ( EXPN_INCAP_LL IS  NOT NULL AND  (N_INCAP_CHGR_UPL IS NOT NULL AND EXPN_INCAP_UPL IS  NULL))
    OR ( EXPN_INCAP_UPL IS NOT  NULL AND (N_INCAP_CHGR_LL IS NOT  NULL  AND  EXPN_INCAP_LL IS  NULL ))
    )) aa
    LEFT JOIN
    (
    SELECT TICKER_SYMBOL, CAST(DATE(ACT_PUBTIME) AS DATETIME) AS TRADE_DATE,
    CAST(END_DATE AS DATETIME) AS END_DATE,
    FISCAL_PERIOD, N_INCOME_ATTR_P AS INCOME_LAST_YEAR
    FROM datayesdb.vw_fdmt_is WHERE PUBLISH_DATE >= '2010-01-01'
    AND MONTH(END_DATE) = FISCAL_PERIOD AND FISCAL_PERIOD = 12
    AND  ACT_PUBTIME IN
    (
    SELECT MAX_PUBTIME AS ACT_PUBTIME FROM (
    SELECT  TICKER_SYMBOL ,DATE_SUB(END_DATE,INTERVAL -1 YEAR) AS END_DATE_NEXT_Y  ,END_DATE,MAX(ACT_PUBTIME) MAX_PUBTIME
    FROM datayesdb.vw_fdmt_is WHERE PUBLISH_DATE >= '2010-01-01'
    AND MONTH(END_DATE) = FISCAL_PERIOD AND FISCAL_PERIOD = 12
    GROUP BY
    TICKER_SYMBOL,
    DATE_SUB(END_DATE,INTERVAL -1 YEAR),
    END_DATE)  TD WHERE MAX_PUBTIME < END_DATE_NEXT_Y
    )
    ) bb
    ON aa.TICKER_SYMBOL=bb.TICKER_SYMBOL
    AND DATE_FORMAT(DATE_SUB(aa.END_DATE,INTERVAL 1 YEAR),'%Y-%m-%d') = DATE_FORMAT(bb.END_DATE,'%Y-%m-%d' )
    AND  aa.TRADE_DATE >bb. TRADE_DATE AND  bb.TRADE_DATE >bb. END_DATE """
    import pandas

    df_fdmt = pandas.read_sql_query(sql, conn)
    pass
    # db = config.mongo.mongo_db
