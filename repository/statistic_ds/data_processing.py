#!usr/bin/env python
# _*_ coding: utf-8 _*_

# 读入数据中有日期信息时,用此函数可以直接处理

import re, os
import sqlite3

from datetime import datetime


def uni_date_format(datestr):
    # 统一日期格式， 将日期str转换为datetime类型
    datepattern = re.compile('(\d\d\d\d).?(\d\d).?(\d\d)')
    try:
        matches = re.search(datepattern, datestr)
        year = matches.group(1)
        month = matches.group(2)
        day = matches.group(3)
        dates = datetime.strptime(year + month + day, '%Y%m%d')
    except:
        dates = ''
    return dates

def get_name(words):
    pt = '(.*[/(<].*[>/)]).*(\d\d:\d\d:\d\d)'

    matches = re.search(pt, words)
    if matches:
        try:
            namestr = matches.group(1).strip()
            # pid = matches.group(2)
        except:
            namestr = ''
    else:
        namestr = words.split(' ')[0]
    return namestr#.split(' ')[0]

def get_name_outof_date(words):
    # try match name from given string
    # pt = '(.*)\s'
    pt = '\s(\w*)\s.*\d\d:\d\d:\d\d\s'

    matches = re.search(pt, words)
    try:
        namestr = matches.group(1).strip()
        #pid = matches.group(2)
    except:
        namestr = ''
        # pid = ''
    # return id QQ
    try:
        uniqueid = matches.group(2).strip()
    except:
        uniqueid = ''
    return namestr,uniqueid # decode

def get_name_outof_time(words):
    # try match name from given string
    pt = '(.*)\s'
    # pt = '(.*)\d\d:\d\d:\d\d'

    matches = re.search(pt, words)
    try:
        namestr = matches.group(1).strip()
        #pid = matches.group(2)
    except:
        namestr = ''
        # pid = ''
    # return id QQ
    try:
        uniqueid = matches.group(2).strip()
    except:
        uniqueid = ''
    return namestr,uniqueid # decode
def get_date(words):
    # try match name from given string
    datepattern = re.compile('\d\d/\\d\d/\\d\d')
    matches = re.findall(datepattern, words)
    try:
        value = matches[0]
    except:
        value = ''
    return value

def getconn(path):
    conn = sqlite3.connect(path)
    try:
        conn = sqlite3.connect(path)
        return conn
    except:
        pass

def getcursor(conn):
    #return conn.cursor()
    try:
        return conn.cursor()
    except:
        pass

def closeconn(conn):
    conn.commit()
    try:
        conn.close()
    except:
        pass

def createtable(db):
    conn = getconn(db)
    sql = """CREATE TABLE records(
                            name TEXT NOT NULL,
                            date  TEXT NOT NULL,
                            PRIMARY KEY (name, date)
                            )"""
    cursor = getcursor(conn)
    cursor.execute(sql)
    conn.commit()
    conn.close()

def store_data(data):
    # 只存储一种格式 名字， 与日期， 表示一次签到记录
    db = 'db.sqlite'

    conn = getconn(db)
    cursor = getcursor(conn)
    sql = '''INSERT INTO records VALUES (?,?)'''
    for d in data:
        #print(d)
        name, date = d[0], d[1]
        # print(type(name))
        #name = name.encode('utf-8')
        # cursor.execute(sql, (name, date))
        try:
            cursor.execute(sql, (name, date))
        except:
            pass
    conn.commit()
    conn.close()
    # closeconn(conn)

def data_clean(filename):

    timepattern = re.compile('\d\d:\d\d:\d\d')
    keypattern = re.compile('签到')
    datesep_pattern = re.compile('Date:(\s+\d\d\d\d\S\d\d\S\d\d)')

    recordkey = ''
    namelist = []
    # 首先尝试从文件名中提取日期
    recorddate = uni_date_format(filename)

    with open(filename,'r') as f:
        line = f.readlines()
        for item in line:
            #判断是否匹配时间格式
            datestr = uni_date_format(item)
            if re.findall(timepattern, item) and recorddate:
                recordkey = get_name(item)
                # if datestr:
                #     recordkey, uid = get_name_outof_date(item)
                # else:
                #     recordkey, uid = get_name_outof_time(item)
                # if uid:
                #     recordkey = recordkey+'('+uid+')'
                # dtmp = uni_date_format(item)
                if datestr:
                    recorddate = datestr
                #print(recordkey)
            # 接着匹配是否有签到
            if recordkey:
                recordflag = re.findall(keypattern, item)
            if recordkey and recorddate:
                namelist.append((recordkey, recorddate))
                print(recordkey)#, recorddate))
                recordkey = ''
            # 匹配是否有日期更新
            if datestr:
                recorddate = datestr
    if namelist:
        store_data(namelist) #数据存入数据库
    #return namelist
## Todo store namelist to db

# get formatted data from db
# neet to import a full name list into store

def travelfolder(rootdir=os.getcwd(),target=''):
    filelist = []
    for (dirpath, dirnames, filenames) in os.walk(rootdir):
        for filename in filenames:
            #filename = filename#.decode('gbk')
            fullname = os.path.join(dirpath,filename)
            data_clean(fullname)
    return filelist

def run():
    # 新建表
    db = 'db.sqlite'
    try:
        createtable(db)
    except:
        pass
    travelfolder('data')

if __name__ == "__main__":
    # 新建表
    db = 'db.sqlite'
    try:
        createtable(db)
    except:
        pass
    travelfolder('data')