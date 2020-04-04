#! usr/bin/python
# coding=utf-8


import crcmod.predefined
import pandas as pd
import numpy as np
from math import isinf, isnan
import string_util
import sys
from decimal import *
from dateutil import tz
from dateutil.tz import tzlocal
from datetime import datetime
import json

reload(sys)
sys.setdefaultencoding('utf-8')


def datetime_2_str(datetime_source, format):
    # if str(type(datetime_source)).lower() in 'datetime64':
    # datetime_source = np.datetime64(datetime_source).astype(datetime)
    # 设置时区
    to_zone = tz.gettz('CST')
    datetime_source = datetime_source.replace(tzinfo=to_zone)
    result = datetime.strftime(datetime_source, format)  # 未发现时间偏移现象，否则这里的CST应该是个灵活的配置
    # print result
    return result


def crc32(source):
    crc32 = crcmod.predefined.Crc('crc-32')
    byte_arr = bytes(source)
    crc32.update(byte_arr)
    return crc32.crcValue
