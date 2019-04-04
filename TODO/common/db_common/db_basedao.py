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

import crcmod.predefined
import numpy as np
import pandas as pd
import crc
from common.config import logger
import string_util as string_util


class DB_BaseDao:

    db_batch_size = 100

    def get_calendar_date(self, conn):
        sql = """
            select 
            convert(int, replace(convert(varchar,t.CALENDAR_DATE,112),'-','')) as END_DATE,
            t.IS_OPEN
            from md_trade_cal t with (nolock) 
            where QA_ACTIVE_FLG = 1 and EXCHANGE_CD = 'XSHG' and  t.CALENDAR_DATE<= getDate()
            order by CALENDAR_DATE
        """
        df_return = pd.read_sql(sql, conn)
        return df_return

    def insert_2_table(self, tablename, df_data, conn):
        # print df_data
        df_data = df_data.where(pd.notnull(df_data), None)
        field_quote = self.get_field_quote(conn)
        cur = conn.cursor()  # <type 'pymssql.Connection'>
        if 'ETL_CRC' not in df_data.columns:
            df_data['ETL_CRC'] = 1
        df_data['QA_ACTIVE_FLG'] = 1
        df_data['CREATE_BY'] = 'Python_etl'
        df_data['CREATE_TIME'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df_data['UPDATE_BY'] = 'Python_etl'
        df_data['UPDATE_TIME'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 将转化为series后，在转化为tuple时，这个字段会变成int64型，插入数据库报错【ValueError: expected a simple type, a tuple or a list】
        # 兼容mysql，将下面这2个字段转换为str，如果再碰到写数据库的问题，不行就就能继承这个方法了
        df_data['ETL_CRC'] = df_data['ETL_CRC'].astype(str)
        df_data['QA_ACTIVE_FLG'] = df_data['QA_ACTIVE_FLG'].astype(str)
        #df_data.drop(['ETL_CRC','QA_ACTIVE_FLG'], axis=1, inplace = True)
        for i in range(len(df_data)):
            row_data = df_data.iloc[i]
            insert_sql = "INSERT INTO %s (%s) VALUES(%s) " % (tablename,
                                                              ','.join([(field_quote + value + field_quote) for value in row_data.index.values]),
                                                              ','.join([str(
                                                                  string_util.value_2_db_desc(row_data.values[j])) for j in range(len(row_data.values))]))
            # 用executemany()
            #tuples = [tuple(row_data.values)]
            #cur.executemany(insert_sql, tuples)
            # 用execute()
            #print insert_sql
            #for i in range(len(row_data.values)):
            #    print type(row_data.iloc[i])
            #print tuple(row_data.values)
            cur.execute(insert_sql, tuple(row_data.values))
            if (i + 1) % self.db_batch_size == 0:
                conn.commit()
                logger.info("insert database, tablename = %s, count = %s" % (tablename, i + 1))
        conn.commit()
        logger.info("insert database, tablename = %s, real_count = %s" % (tablename, len(df_data)))
        cur.close()

    def update_2_table(self, tablename, df_data, uniq_keys, conn):
        if df_data is not None and len(df_data) > 0:
            #logger.info("update database count = %s" % len(df_data))
            field_quote = self.get_field_quote(conn)
            cur = conn.cursor()
            df_data = df_data.where(pd.notnull(df_data), None)
            df_data['QA_ACTIVE_FLG'] = 1
            df_data['UPDATE_BY'] = 'Python_etl_u'
            df_data['UPDATE_TIME'] = datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S')
            df_data['ETL_CRC'] = df_data['ETL_CRC'].astype(str)
            df_data['QA_ACTIVE_FLG'] = df_data['QA_ACTIVE_FLG'].astype(str)
            for i in range(len(df_data)):
                row_data = df_data.iloc[i]
                row_data_where = pd.Series(
                    [row_data[value] for value in uniq_keys], index=uniq_keys)
                row_data_value = row_data.drop(uniq_keys)
                update_sql = "update %s set %s where %s " % (tablename,
                                                             ','.join([('%s%s%s = ' % (field_quote,
                                                                                       key,
                                                                                       field_quote)) + str(
                                                                 string_util.value_2_db_desc(value)) for key,
                                                                                                         value in row_data_value.iteritems()]),
                                                             ' and '.join([('%s%s%s %s ' % (field_quote,
                                                                                            key,
                                                                                            field_quote,
                                                                                            '=' if value is not None else 'is')) + str(
                                                                 string_util.value_2_db_desc(value)) for key,
                                                                                                         value in row_data_where.iteritems()]))
                #print update_sql
                tuple_value = tuple(row_data_value.append(row_data_where))
                #print tuple_value
                cur.execute(update_sql, tuple_value)
                #print update_sql
                if (i + 1) % self.db_batch_size == 0:
                    conn.commit()
                    logger.info("update database, tablename = %s, real_count = %s" % (tablename, i + 1))
            conn.commit()
            logger.info("update database, tablename = %s, real_count = %s" % (tablename, len(df_data)))
            cur.close()

    def merge_2_table_force_update(self,tablename,df_data,arr_where_fields,arr_select_fields,where_condition,conn):
        """
        这里更新数据库qa_manual_flg is null and etl_crc != etl_crc_db的的数据
        比上面的少个qa_active_flg 的条件
        :param tablename:
        :param df_data:
        :param arr_where_fields:
        :param arr_select_fields:
        :param where_condition:
        :param conn:
        :return:
        """
        if df_data is not None and len(df_data) > 0:
            df_data_db = self.get_data_from_table(tablename, arr_select_fields, where_condition,conn)
            df_data['ETL_CRC'] = df_data.apply(crc.row_2_crc32, columns=df_data.columns, axis=1)
            #df_data['ETL_CRC'] = df_data['ETL_CRC'].astype('str')
            df_data_merge = df_data.merge(
                df_data_db,
                how='left',
                left_on=arr_where_fields,
                right_on=arr_where_fields,
                suffixes=('','_2'),
                left_index=False)
            df_data_insert = df_data_merge[df_data_merge['ETL_CRC_db'].astype(str) == 'nan']
            df_data_insert.drop(['ETL_CRC_db', 'QA_ACTIVE_FLG_db', 'QA_MANUAL_FLG_db'], axis=1, inplace=True)
            df_data_update = df_data_merge[
                (~df_data_merge['ETL_CRC_db'].isnull()) &
                (df_data_merge['ETL_CRC'] != df_data_merge['ETL_CRC_db']) &
                (df_data_merge['QA_MANUAL_FLG_db'].isnull())]
            df_data_update.drop(['ETL_CRC_db', 'QA_ACTIVE_FLG_db', 'QA_MANUAL_FLG_db'], axis=1, inplace=True)
            if df_data_insert is not None and len(df_data_insert) > 0:
                self.insert_2_table(tablename, df_data_insert,conn)
            if df_data_update is not None and len(df_data_update) > 0:
                self.update_2_table(tablename, df_data_update, arr_where_fields,conn)

    def merge_2_table(self, tablename, df_data, uniq_keys, arr_select_fields, where_condition, conn):
        if df_data is not None and len(df_data) > 0:
            df_data_db = self.get_data_from_table(tablename, arr_select_fields, where_condition,conn)
            df_data['ETL_CRC'] = df_data.apply(crc.row_2_crc32, columns=df_data.columns, axis=1)
            #df_data['ETL_CRC'] = df_data['ETL_CRC'].astype('str')
            df_data_merge = df_data.merge(
                df_data_db,
                how='left',
                left_on=uniq_keys,
                right_on=uniq_keys,
                suffixes=('','_2'),
                left_index=False)
            df_data_insert = df_data_merge[df_data_merge['ETL_CRC_db'].astype(str) == 'nan']
            df_data_insert.drop(['ETL_CRC_db', 'QA_ACTIVE_FLG_db', 'QA_MANUAL_FLG_db'], axis=1, inplace=True)
            df_data_update = df_data_merge[
                (~df_data_merge['ETL_CRC_db'].isnull()) &
                (df_data_merge['ETL_CRC'] != df_data_merge['ETL_CRC_db']) &
                (df_data_merge['QA_ACTIVE_FLG_db'] == 1) &
                (df_data_merge['QA_MANUAL_FLG_db'].isnull())]
            df_data_update.drop(['ETL_CRC_db', 'QA_ACTIVE_FLG_db', 'QA_MANUAL_FLG_db'], axis=1, inplace=True)
            if df_data_insert is not None and len(df_data_insert) > 0:
                self.insert_2_table(tablename, df_data_insert,conn)
            if df_data_update is not None and len(df_data_update) > 0:
                self.update_2_table(tablename, df_data_update, uniq_keys,conn)


    def get_data_from_table(self,tablename,arr_select_fields,where_condition,conn):
        table_lock = self.get_table_lock(conn)
        sql = """
        select
        {fields}
        ETL_CRC as ETL_CRC_db,
        QA_ACTIVE_FLG as QA_ACTIVE_FLG_db,
        QA_MANUAL_FLG as QA_MANUAL_FLG_db
        from {tablename} t {table_lock}
        {where_condition}
        """.format(tablename=tablename, where_condition=where_condition, fields=''.join([(value + ',') for value in arr_select_fields]), table_lock=table_lock)
        # print sql
        df_return = pd.read_sql(sql, conn)
        df_return['ETL_CRC_db'] = df_return['ETL_CRC_db'].fillna(1)
        return df_return

    def get_table_lock(self, conn):
        table_lock = ''
        if 'mssql' in str(type(conn)).lower():
            table_lock = ' with (nolock) '
        return table_lock

    def get_field_quote(self, conn):
        """
        mysql的字段是关键字时，需要将字段用该方法处理
        :param conn:
        :return:
        """
        field_quote = ''
        if 'mysql' in str(type(conn)).lower():
            field_quote = '`'
        return field_quote


