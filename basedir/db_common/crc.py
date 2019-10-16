#! usr/bin/python
# coding=utf-8

##########################################################################
# 通联数据机密
# -------------------------------------------------------------------------
# 通联数据股份公司版权所有 © 2013-2017
#
# 注意：本文所载所有信息均属于通联数据股份公司资产。本文所包含的知识和技术概念均属于
# 通联数据产权，并可能由中国、美国和其他国家专利或申请中的专利所覆盖，并受商业秘密或
# 版权法保护。
# 除非事先获得通联数据股份公司书面许可，严禁传播文中信息或复制本材料。
#
# DataYes CONFIDENTIAL
# ----------------------------------------------------------------------------
# Copyright @ 2013-2016 DataYes, All Rights Reserved.
#
# NOTICE:  All information contained herein is the property of DataYes
# Incorporated. The intellectual and technical concepts contained herein are
# proprietary to DataYes Incorporated, and may be covered by China, U.S. and
# Other Countries Patents, patents in process, and are protected by trade
# secret or copyright law.
# Dissemination of this information or reproduction of this material is
# strictly forbidden unless prior written permission is obtained from DataYes.
##########################################################################

import crcmod.predefined
import pandas as pd
import numpy as np
from math import isinf,isnan
import string_util
import sys
from decimal import *
from dateutil import tz
from dateutil.tz import tzlocal
from datetime import datetime
import json

reload(sys)
sys.setdefaultencoding('utf-8')

def row_2_crc32(row, columns, column_type_map = None):
    """
    row: 单个记录行
    columns: 数组，行对应的列名
    column_type_map: 字段和类型map，如：{'SECURITY_ID':'str'}，先实现这种，如果有需要自定义的转换，再实现下面这种同时，需要兼容这种参数方式
    column_type_map: 字段和类型map，如：{'SECURITY_ID':{'field_type':'str','func':None}
    """
    if columns is None or len(columns) == 0:
        return np.nan
    else:
        str_tmp = ''
        for index in range(len(columns)):
            # print index
            # print columns[index]
            temp = str(row[columns[index]]) if (column_type_map is None or len(column_type_map) == 0) else value_2_str(row[columns[index]], column_type_map[columns[index]])
            str_tmp += temp
            # # print type(series[columns[i]])
        #print str_tmp
        # # print series.dtype
        #return str_tmp
        return crc32(str_tmp)



def value_2_str(value, field_type):
    #print field_type
    #print type(field_type)
    #field_type = str(field_type)

    # print value
    if type(field_type) == dict : #datatime 类型处理    #and field_type.has_key('field_type')
        if(field_type['field_type'] == 'datetime'):
            return datetime_2_str(value, field_type['format'])
        else:
            return str(value)
    else:   #兼容不传field_type
        field_type = str(field_type)
        if field_type == 'object' or field_type == 'str':
            if string_util.is_null(value):
                if str(value).lower() == 'none':    # 字符串空，返回null
                    return 'null'
                elif str(value).lower() == 'nan' or isnan(value) or isinf(value):   # 数字空，返回NULL
                    return 'NULL'
            else:
                return str(value)
        elif 'int' in field_type.lower() or 'long' in field_type.lower():
            return str(int(value))
        elif 'float' in field_type.lower():   # 这个可能要特殊处理
            if str(value).lower() == 'none':  # 字符串空，返回null
                return 'null'
            elif str(value).lower() == 'nan' or isnan(value) or isinf(value):  # 数字空，返回NULL
                return 'NULL'
            else:
                return str(value)
        elif 'decimal' in field_type.lower():
            if str(value).lower() == 'none':  # 字符串空，返回null
                return 'null'
            elif str(value).lower() == 'nan' or isnan(value) or isinf(value):  # 数字空，返回NULL
                return 'NULL'
            else:
                # talend做法：小数位全部是0，去除小数部分；如果这个值是以0结尾，则使用科学计数，其余情况仍使用原始的数
                # 特殊处理999999999999999999999999999999.99999999极大值、极小值和0.00000000
                if value == 0 or value > getcontext().Emax or value < getcontext().Emin:
                    return str(value)
                else:
                #print value.normalize()
                #print str(Decimal(value).normalize())
                    return str(value.normalize())
                # 指定sql查询的coerce_float属性后，查询的字段表示与java一直
                #return decimal_2_str(value)
                #return str(Decimal(value).normalize()) #这个方法不行，有些超长的decimal字段，转化后与java不一致
        elif 'datetime' in field_type.lower():  # datatime 类型；目测还需要一些测试用例
            #print field_type.lower()
            return datetime_2_str(value, '%a %b %d %H:%M:%S %Z %Y')
        elif 'date' in field_type.lower():
            return str(value)
        else:
            return str(value)


def datetime_2_str(datetime_source, format):
    #if str(type(datetime_source)).lower() in 'datetime64':
    #datetime_source = np.datetime64(datetime_source).astype(datetime)
    # 设置时区
    to_zone = tz.gettz('CST')
    datetime_source = datetime_source.replace(tzinfo=to_zone)
    result = datetime.strftime(datetime_source, format) # 未发现时间偏移现象，否则这里的CST应该是个灵活的配置
    #print result
    return result


def crc32(source):
    crc32 = crcmod.predefined.Crc('crc-32')
    byte_arr = bytes(source)
    crc32.update(byte_arr)
    return crc32.crcValue
