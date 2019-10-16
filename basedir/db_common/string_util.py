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

import datetime
import calendar
import pandas as pd
import uuid


def get_uuid():
    """
    生成32位uuid
    参考：https://www.cnblogs.com/dkblog/archive/2011/10/10/2205200.html
    """
    return str(uuid.uuid1()).replace('-','')

def getFormatNDay(ndays, format):
    """
    ndays:
    format:
    example:stringUtil.getFormatNDay(-30,'%Y%m%d')
    返回string
    获取当前时间几天前的时间
    """
    nowtime = datetime.datetime.now() + datetime.timedelta(days=ndays)
    return nowtime.strftime(format)


def getFormatDay(dateStr, formatOld, formatNew):
    """
    ndays:
    format:
    example:stringUtil.getFormatNDay(-30,'%Y%m%d')
    返回string
    将时间规格化
    """
    return datetime.datetime.strptime(dateStr, formatOld).strftime(formatNew)


def getNDay(dateStr, format, ndays):
    """
    获取传入时间N天前的时间
    """
    date = datetime.datetime.strptime(dateStr, format) + datetime.timedelta(ndays)
    return date.strftime(format)


def getNDaysBetweenDate(dateStr1, format1, dateStr2, format2):
    """
    获取两个日期相差的天数，大的日期在前
    返回int
    """
    date1 = datetime.datetime.strptime(dateStr1, format1)
    date2 = datetime.datetime.strptime(dateStr2, format2)
    return int((date1 - date2).days)


def getDayNMonths(dateStr, format, nMonths):
    """
    nMonths:参数传入的是正数表示往后 ，负数表示往前
    获取传入时间N个月的时间
    """
    date = datetime.datetime.strptime(dateStr, format)
    month = date.month - 1 + nMonths
    year = date.year + month / 12
    month = month % 12 + 1
    day = min(date.day, calendar.monthrange(year, month)[1])
    date = date.replace(year=year, month=month, day=day)
    return date.strftime(format)


def getYearFirstDay(dateStr, format):
    """
    获取年的第一天，返回string
    """
    date = datetime.datetime.strptime(dateStr, format)
    return date.strftime('%Y') + '0101'


def getMonthFirstDay(dateStr,format):
    """
    获取月的第一天
    """
    date = datetime.datetime.strptime(dateStr,format)
    return date.strftime('%Y%m') + '01'


def getWeekFirstDay(dateStr,format):
    """
    获取周的第一天
    """
    vdate = datetime.datetime.strptime(dateStr,format)
    dayscount = datetime.timedelta(days=vdate.isoweekday())
    dayfrom = vdate - dayscount + datetime.timedelta(days=1)
    return dayfrom.strftime('%Y%m%d')


def dateRange(start, end, step=1, format="%Y%m%d"):
    """
    生成日期序列
    """
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(str(end), format) - strptime(str(start), format)).days
    return [int(strftime(strptime(str(start), format) + datetime.timedelta(i), format)) for i in xrange(0, days, step)]


def value_2_db_desc(value):
    db_desc = '%s'
    if 'int' in str(type(value)).lower() or 'long' in str(type(value)).lower():
        db_desc = '%d'
    elif 'float' in str(type(value)).lower():
        db_desc = '%s'
    # print ('%s -- %s --%s') %( value,db_desc,type(value))
    return db_desc

"""
def value_2_db_value(value):
    db_desc = 'null'
    if value is None:
        db_desc = 'null'
    elif 'int' in str(type(value)).lower() or 'long' in str(type(value)).lower():
        db_desc = '%d' % value
    elif 'float' in str(type(value)).lower():
        db_desc = '%f' % value
    else:
        db_desc = ("'%s'" % value)
    # print ('%s -- %s --%s') %( value,db_desc,type(value))
    return db_desc
"""

def is_empty(input_obj):
    if input_obj is None or str(input_obj).lower() == '' or str(input_obj).lower() == 'nan' or str(input_obj).lower() == 'none':
        return True
    else:
        return False

def is_null(input_obj):
    if input_obj is None or str(input_obj).lower() == 'nan' or str(input_obj).lower() == 'none':
        return True
    else:
        return False

def cal_end_date_dimension(end_date):
    """
    根据end_date日期，计算相关的时间维度数据

    :param end_date:传入的日期，格式如20170929，int型
    :return:
    """
    row_end_date_dimension = pd.Series()
    row_end_date_dimension['END_DATE'] = end_date
    row_end_date_dimension['END_DATE_1D'] = int(getNDay(str(end_date), '%Y%m%d', -1))
    row_end_date_dimension['END_DATE_1W'] = int(getNDay(str(end_date),'%Y%m%d',-7))
    row_end_date_dimension['END_DATE_1M'] = int(getDayNMonths(str(end_date),'%Y%m%d',-1))
    row_end_date_dimension['END_DATE_3M'] = int(getDayNMonths(str(end_date),'%Y%m%d',-3))
    row_end_date_dimension['END_DATE_6M'] = int(getDayNMonths(str(end_date),'%Y%m%d',-6))
    row_end_date_dimension['END_DATE_YTD'] = int(getYearFirstDay(str(end_date),'%Y%m%d'))
    row_end_date_dimension['END_DATE_1Y'] = int(getDayNMonths(str(end_date),'%Y%m%d',-12))
    row_end_date_dimension['END_DATE_2Y'] = int(getDayNMonths(str(end_date),'%Y%m%d',-12 * 2))
    row_end_date_dimension['END_DATE_3Y'] = int(getDayNMonths(str(end_date),'%Y%m%d',-12 * 3))
    row_end_date_dimension['END_DATE_5Y'] = int(getDayNMonths(str(end_date),'%Y%m%d',-12 * 5))

    row_end_date_dimension['END_DATE_MTD'] = int(getMonthFirstDay(str(end_date),'%Y%m%d'))
    row_end_date_dimension['END_DATE_WTD'] = int(getWeekFirstDay(str(end_date),'%Y%m%d'))
    #row_md_trade_cal = df_md_trade_cal.loc[end_date]
    #row_end_date_dimension = row_end_date_dimension.append(row_md_trade_cal)
    return row_end_date_dimension
