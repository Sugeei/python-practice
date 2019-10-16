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
print('config')
print(this_dir)
# run config.py, this_dir will be root.../common

base_dir = os.path.dirname(this_dir)

