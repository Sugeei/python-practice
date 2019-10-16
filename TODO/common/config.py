#! usr/bin/python
# coding=utf-8

from logging import config
import json
import logging
import os
import re
import sys
import pymssql
import pymysql
import pika
import pymongo
import yaml
from collections import namedtuple

# from common.logger import logger
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
# run config.py, this_dir will be root.../common

base_dir = os.path.dirname(this_dir)
wechat_server = "http://114.215.238.50:8080/webcrawl/wechat/sendMsg?" \
                "roboId=3319122883"


def determine_home():
    if "DATA_PROD_HOME" in os.environ:
        return os.environ['DATA_PROD_HOME']
    else:
        cur_dir = base_dir
        while cur_dir != "/":
            if cur_dir.endswith(u"dataifs-data-production") \
                    or cur_dir.endswith(u"data-production-home"):
                return cur_dir
            else:
                cur_dir = os.path.dirname(cur_dir)
    return base_dir


home_dir = determine_home()


def determine_module():
    if "PROD_MODULE" in os.environ:
        return os.environ["PROD_MODULE"]
    else:
        module_dir = os.path.dirname(sys.modules['__main__'].__file__)
        return module_dir[module_dir.rfind('/') + 1:]



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
        # for 米内网数据
        self.health_db = MssqlConn(
            os.environ['HEALTH_DB']) if 'HEALTH_DB' in os.environ else None

        self.bigdata_db = MssqlConn(
            os.environ['BIG_DATA_DB']) if 'BIG_DATA_DB' in os.environ else None

        self.mssql_db = MssqlConn(
            os.environ['DY_DB_RW']) if 'DY_DB_RW' in os.environ else None
        self.datayes_db_ro = MssqlConn(
            os.environ['DY_DB_RO']) if 'DY_DB_RO' in os.environ else None

        self.cdc_db = MssqlConn(
            os.environ['CDC_DB']) if 'CDC_DB' in os.environ else None

        self.wechat_contactor = json.loads(os.environ['WECHAT_CONTACTOR']) \
            if 'WECHAT_CONTACTOR' in os.environ \
               and str(os.environ['WECHAT_CONTACTOR']) != '' else {}

        self.wechat_server = wechat_server if 'WECHAT_SERVER' not in \
                                              os.environ \
            else os.environ['WECHAT_SERVER']

        self.mysql_db = MysqlConn(
            os.environ['TALEND_DB']) if 'TALEND_DB' in os.environ else None

        self.ashare_mssql_db = MssqlConn(os.environ['ASHARE_DB_RO']) \
            if 'ASHARE_DB_RO' in os.environ else None

        self.uts_mssql_db = MssqlConn(
            os.environ['UTS_DB_RO']) if 'UTS_DB_RO' in os.environ else None

        self.uts_client_mssql_db = MssqlConn(os.environ['UTS_CLIENT_DB_RO']) \
            if 'UTS_CLIENT_DB_RO' in os.environ else None

        self.mis_ehr_mssql_db = MssqlConn(os.environ['MIS_EHR_DB_RO']) \
            if 'MIS_EHR_DB_RO' in os.environ else None

        self.analyst_mssql_db = MssqlConn(os.environ['FUNDRISKCONTROL_DB_RO']) \
            if 'FUNDRISKCONTROL_DB_RO' in os.environ else None

        self.macr_mssql_db = MssqlConn(
            os.environ['MACR_DB_RO']) if 'MACR_DB_RO' in os.environ else None

        self.security_db = MysqlConn(
            os.environ['DB_SECURITY']) if 'DB_SECURITY' in os.environ else None

        self.intelligence0_db = MysqlConn(os.environ['INTELLIGENCE_DB_RW']) \
            if 'INTELLIGENCE_DB_RW' in os.environ else None

        self.rrp_bigdata_ro = MysqlConn(os.environ['RRP_BIGDATA_RO']) \
            if 'RRP_BIGDATA_RO' in os.environ else None

        self.rrp_bigdata_db = MysqlConn(os.environ['RRP_BIGDATA_DB_RW']) \
            if 'RRP_BIGDATA_DB_RW' in os.environ else None

        self.researchrpt = MysqlConn(os.environ['RESEARCHRPT_DB']) \
            if 'RESEARCHRPT_DB' in os.environ else None

        self.researchrpt_src = MysqlConn(
            os.environ['RESEARCHRPT_DB_SRC']) if 'RESEARCHRPT_DB_SRC' in os.environ else None

        self.rrp_bigdata_db = MysqlConn(os.environ['RRP_BIGDATA_DB_RW']) if 'RRP_BIGDATA_DB_RW' in os.environ else None

        self.jymsql_db = MssqlConn(
            os.environ['JY_DB']) if 'JY_DB' in os.environ else None

        # format: server1:port,server2:port2,server3:port3
        self.kafka_conn = os.environ['KAFKA'] if 'KAFKA' in os.environ \
            else None

        self.mongo = MongoConn(os.environ['DATAIFS_MONGO_RW']) \
            if 'DATAIFS_MONGO_RW' in os.environ else None

        # example: http://10.21.137.128:8081
        self.schema_registry = None if 'SCHEMA_REGISTRY' not in os.environ \
            else os.environ['SCHEMA_REGISTRY']

        self.rp_mq = MqConn(
            os.environ['RP_MQ']) if 'RP_MQ' in os.environ else None

        self.activate_third_mq = True if 'ACTIVATE_THIRD_MQ' in os.environ \
                                         and 'True' == os.environ[
                                             'ACTIVATE_THIRD_MQ'] else False

        self.ali_mq = MqConn(
            os.environ['ALI_MQ']) if 'ALI_MQ' in os.environ else None

        self.rp_macro_exchange = os.environ.get('RP_MACRO_EXCHANGE',
                                                'eco_change')

        self.api_token = "" if 'TOKEN' not in os.environ else os.environ[
            'TOKEN']

        self.dymysql_db = MysqlConn(
            os.environ['PRD_DB_RO']) if 'PRD_DB_RO' in os.environ else None

        self.riskmdl_db = MysqlConn(
            os.environ['RISKMDL_DB']) if 'RISKMDL_DB' in os.environ else None

        self.mail_source = json.loads(
            os.environ['MAIL_HOST']) if 'MAIL_HOST' in os.environ else ""

        # 中债数据库
        # prd:{"server":"sh-datamall-db02.datayes.com","port":1433,
        # "database":"chinabond","user":"dataops_rw","password":"Welcome@668",
        # "charset":"utf8","tds_version":"7.0"}
        self.chinabond_db = MssqlConn(os.environ['CHINABOND_DB_RO']) \
            if 'CHINABOND_DB_RO' in os.environ else None

        # 证监会基金接入数据库
        self.csrc_db = MssqlConn(
            os.environ['CSRC_DB_RW']) if 'CSRC_DB_RW' in os.environ else None

        # datayes release db(73)
        # prd:{"server":"10.21.139.73","port":1433,"database":"datayesdb",
        # "user":"uts_sync","password":"uts_sync","charset":"utf8",
        # "tds_version":"7.0"}
        self.dy_re_db = MssqlConn(
            os.environ['RE_DB_RO']) if 'RE_DB_RO' in os.environ else None

        # api数据表对应的数据库，通称产品库
        # prd_ro:{"host":"db-datayesdb-ro.wmcloud.com","port":3313,
        # "user":"uts_sync","passwd":"i1lj8Zwit7Eg9SFj","db":"data_api",
        # "charset":"utf8"}
        self.dataapi_product_db = MysqlConn(
            os.environ[
                'DATAAPI_PRODUCT_DB']) \
            if 'DATAAPI_PRODUCT_DB' in os.environ else None

        # api的配置数据库
        # prd:{"host":"10.21.232.162","port":3306,"user":"app_talend_ro",
        # "passwd":"yULN9LZ01G72PbUK","db":"apicfg","charset":"utf8"}
        self.api_cfg_db = MysqlConn(os.environ['API_CONFIG_DB']) \
            if 'API_CONFIG_DB' in os.environ else None

        # 宏观数据库
        # prd:{"server":"sh-dm-db05.datayes.com","port":1433,
        # "database":"dyedb",
        # "user":"talend_load","password":"s9t5gNThn2vqWM7c","charset":"utf8",
        # "tds_version":"7.0"}
        self.dyedb_db = MssqlConn(
            os.environ['DYEDB_DB']) if 'DYEDB_DB' in os.environ else None

    def add_cdc_table(self, database, table, status):
        self.mongo.mongo_db.cdc_tables.find_one_and_update(
            filter={"database": database, "table": table},
            update={"$set": {"status": status}},
            upsert=True)
        logger.info("add/update cdc table: %s %s" % (database, table))

    def turn_on_cdc_table(self, database, table):
        self.mongo.mongo_db.cdc_tables.find_one_and_update(
            filter={"database": database, "table": table},
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
        doc = self.mongo.mongo_db.cdc_tables.find_one(
            filter={"database": database, "table": table})
        return doc['lp'] if doc is not None and 'lp' in doc else None

    def set_cdc_table_lp(self, database, table, lp):
        self.mongo.mongo_db.cdc_tables.find_one_and_update(
            filter={"database": database, "table": table},
            update={"$set": {"lp": lp}})


class MongoConn(object):
    def __init__(self, mongo_url):
        mongo_conn = pymongo.MongoClient(mongo_url, connect=False)
        last_slash = mongo_url.rfind('/')
        last_que = mongo_url.rfind('?')
        db_name = mongo_url[last_slash + 1:last_que] \
            if last_que > last_slash else mongo_url[last_slash + 1:]
        self.mongo_db = mongo_conn.get_database(db_name)
        logger.info("mongo connection creation with url = %s" % mongo_url)


class MysqlConn(object):
    def __init__(self, config_json_str):
        self.mysql_config = json.loads(config_json_str, encoding='utf-8')

    def connect(self):
        mysql_conn = pymysql.connect(**self.mysql_config)  # pymysql
        logger.info(
            "mysql connection creation with config = %s" % self.mysql_config)
        return mysql_conn


class MssqlConn(object):
    def __init__(self, config_json_str):
        self.mssql_config = json.loads(config_json_str, encoding='utf-8')

    def connect(self):
        mssql_conn = pymssql.connect(**self.mssql_config)
        logger.info(
            "mssql connection creation with config = %s" % self.mssql_config)
        return mssql_conn

    def __str__(self):
        return json.dumps(self.mssql_config, ensure_ascii=False,
                          encoding='utf-8')

class MqConn(object):
    def __init__(self, mq_url):
        # format: username:password@host:port/virtual_host
        m = re.match(MQ, mq_url)
        self.mq = {"host": m.group("host"), "port": int(m.group("port")),
                   "username": m.group("username"),
                   "password": m.group("password"),
                   "virtual_host": m.group("virtual_host")}
        self.virtual_host = None if (self.mq['virtual_host'] is None or len(
            self.mq['virtual_host']) == 0) \
            else self.mq['virtual_host']
        self.channel = None

    def connect(self):
        logging.info(
            u"trying to connect mq with configuration %s" % self.__str__())
        rp_mq = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.mq['host'],
                                      port=self.mq['port'],
                                      virtual_host=self.virtual_host,
                                      credentials=pika.PlainCredentials(
                                          self.mq['username'],
                                          self.mq['password'])))
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


def get_mail_cfg():
    default_mail_cfg = {
        "host": "idccellopoint.datayes.com",
        "port": 587,
        "username": "svc-pipeline@datayes.com",
        "password": "Wmcl0ud@2018"
    }
    # 如果系统环境变量配置里存在MAIL_CFG，则使用该变量配置；否则使用这里硬编码的邮件配置。
    # MAIL_CFG（如果存在），是把上述配置做成JSON串。
    mail_cfg = default_mail_cfg if "MAIL_CFG" not in os.environ \
        else json.dumps(os.environ['MAIL_CFG'])
    return MailCfg(**mail_cfg)
