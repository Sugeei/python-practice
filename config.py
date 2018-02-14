#! usr/bin/python
# coding=utf-8

# import json
# import pymssql
# import MySQLdb
# import pymongo
# import os
# # from db import MssqlConn
# import yaml
# import logger
# import sys
from logger import config
import json
import logger
import os
import re
import sys
# from logger import config
import pymysql
import pymssql
# import MySQLdb
import pika
import pymongo
import yaml

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
with open(this_dir + "/logger.yaml") as f:
    ycfg = yaml.load(f)
    ycfg.setdefault('version', 1)
    logger.config.dictConfig(ycfg)

main_module = sys.modules['__main__'].__file__
module_dir = os.path.dirname(main_module)
logger_name = module_dir[module_dir.rfind('/') + 1:]
# print "main module is %s, logger name is %s" % (main_module, logger_name)
# logger = logger.basicConfig(filename='fundtags.logs', level=logger.WARNING)
print "main module is %s, logger name is %s" % (main_module, logger_name)
logger = logger.getLogger(logger_name)

