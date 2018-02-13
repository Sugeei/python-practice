#! usr/bin/python
# coding=utf-8

# import json
# import pymssql
# import MySQLdb
# import pymongo
# import os
# # from db import MssqlConn
# import yaml
# import logging
# import sys
from logging import config
import json
import logging
import os
import re
import sys
# from logging import config
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
with open(this_dir + "/logging.yaml") as f:
    ycfg = yaml.load(f)
    ycfg.setdefault('version', 1)
    logging.config.dictConfig(ycfg)

main_module = sys.modules['__main__'].__file__
module_dir = os.path.dirname(main_module)
logger_name = module_dir[module_dir.rfind('/') + 1:]
# print "main module is %s, logger name is %s" % (main_module, logger_name)
# logger = logging.basicConfig(filename='fundtags.logs', level=logging.WARNING)
print "main module is %s, logger name is %s" % (main_module, logger_name)
logger = logging.getLogger(logger_name)

