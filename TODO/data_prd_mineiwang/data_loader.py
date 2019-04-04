#!env /bin/python
# -*- coding: utf-8 -*-
# 通联数据机密
# --------------------------------------------------------------------
# 通联数据股份公司版权所有 © 2013-1016
#
# 注意：本文所载所有信息均属于通联数据股份公司资产。本文所包含的知识和技术概念均属于
# 通联数据产权，并可能由中国、美国和其他国家专利或申请中的专利所覆盖，并受商业秘密或
# 版权法保护。
# 除非事先获得通联数据股份公司书面许可，严禁传播文中信息或复制本材料。
#
# DataYes CONFIDENTIAL
# --------------------------------------------------------------------
# Copyright © 2013-2016 DataYes, All Rights Reserved.
#
# NOTICE: All information contained herein is the property of DataYes
# Incorporated. The intellectual and technical concepts contained herein are
# proprietary to DataYes Incorporated, and may be covered by China, U.S. and
# Other Countries Patents, patents in process, and are protected by trade
# secret or copyright law.
# Dissemination of this information or reproduction of this material is
# strictly forbidden unless prior written permission is obtained from DataYes.

import json
import pymssql
import sys
import time
import traceback

import pandas as pd
import numpy as np
import pymysql


CONFIG_PATH = './config.json'


class DBConn(object):
    def __init__(self, config_path=CONFIG_PATH):
        self.config = DBConn.file2dict(config_path)
        # self.report_research = self.config['report_research']
        # self.report_subtable = self.config['report_subtable']

    @staticmethod
    def file2dict(path):
        with open(path) as f:
            return json.load(f)

    def mysql_connection(self, conn_type=""):
        conn = pymysql.connect(**self.config['conn_type'])
        return conn

    def get_df(self, conn_type, sql):
        # t1 = time.time()
        valid = False
        df = None
        while not valid:
            try:
                conn = self.create_connection(conn_type=conn_type)
                df = pd.read_sql(sql, conn)
                valid = True
                conn.close()
            except Exception as e:
                self.create_connection(conn_type=conn_type)
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
                print('[{0}] sql error:{1}'.format(conn_type, sql))
                time.sleep(5)
        # print('type:{0} cost:{1:.2f}, sql:{2}'.format(conn_type, time.time()-t1, sql))
        return df
