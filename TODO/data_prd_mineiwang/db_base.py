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
from common.config import logger
from data_prd_mineiwang.add_crc import add_crc

# from scattered_scripts.crc_check.lib_com import string_util as string_util


class DB_Base:
    db_batch_size = 100

    def tuple_Getter(self, x):
        for i in range(len(x)):
            if str(type(x[i])) == "<type 'numpy.int64'>" or str(
                    type(x[i])) == "<class 'pandas.tslib.Timestamp'>" or str(
                    type(x[i])) == "<type 'numpy.float64'>":  # str(type(x[i])) == "<class 'numpy.int64'>":
                x[i] = str(x[i]).decode('utf-8')
            elif str(x[i]).lower() == 'nan' or str(x[i]) == 'none':
                x[i] = None
            else:
                x[i] = str(x[i]).decode('utf-8')
        return tuple(x)

    def insert_2_table(self, tablename, df_data, conn):
        # print df_data
        df_data = df_data.where(pd.notnull(df_data), None)
        field_quote = self.get_field_quote(conn)
        cur = conn.cursor()  # <type 'pymssql.Connection'>
        if 'ETL_CRC' not in df_data.columns:
            df_data['ETL_CRC'] = 1
        df_data['INSERT_TIME'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df_data['UPDATE_TIME'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df_data['ETL_CRC'] = df_data['ETL_CRC'].astype(str)
        for i in range(len(df_data)):
            db_batch_size = 200
            row_data = df_data.iloc[i]
            insert_sql = "INSERT INTO %s (%s) VALUES(%s) " % (tablename,
                                                              ','.join(
                                                                  [(field_quote + value + field_quote) for value in
                                                                   row_data.index.values]),
                                                              ','.join(['%s' for i in range(len(row_data.values))]))
            # 用executemany()
            # tuples = [tuple(row_data.values)]
            # cur.executemany(insert_sql, tuples)
            tuples = self.tuple_Getter(row_data.values)
            try:
                cur.execute(insert_sql, tuples)
                # conn.commit()
            except Exception as Error:
                print('Error: ', Error)
            if (i + 1) % db_batch_size == 0:
                conn.commit()
                logger.info("insert database count = %s" % (i + 1))
        conn.commit()
        logger.info("insert database real_count = %s" % (len(df_data)))
        cur.close()

    def insert_table(self, tablename, df_data, union_keys, conn):
        # print df_data
        df_data = df_data.where(pd.notnull(df_data), None)
        field_quote = self.get_field_quote(conn)
        cur = conn.cursor()  # <type 'pymssql.Connection'>
        if 'ETL_CRC' not in df_data.columns:
            df_data['ETL_CRC'] = 1
        df_data['CREATE_TIME'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # df_data_merge['CREATE_TIME'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df_data['UPDATE_TIME'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df_data['ETL_CRC'] = df_data['ETL_CRC'].astype(str)
        for i in range(len(df_data)):
            db_batch_size = 200
            row_data = df_data.iloc[i]
            insert_sql = "INSERT INTO %s (%s) VALUES(%s) " % (tablename,
                                                              ','.join(
                                                                  [(field_quote + value + field_quote) for value in
                                                                   row_data.index.values]),
                                                              ','.join(['%s' for i in range(len(row_data.values))]))
            # 用executemany()
            # tuples = [tuple(row_data.values)]
            # cur.executemany(insert_sql, tuples)
            tuples = self.tuple_Getter(row_data.values)
            try:
                cur.execute(insert_sql, tuples)
                logger.debug("insert database %s" % (row_data[union_keys]))
            except Exception as Error:
                logger.warning('Error: ', Error)
            if (i + 1) % db_batch_size == 0:
                conn.commit()
                logger.info("insert database count = %s" % (i + 1))
        conn.commit()
        logger.info("insert database real_count = %s" % (len(df_data)))
        cur.close()

    def update_2_table(self, tablename, df_data, uniq_keys, conn):
        if df_data is not None and len(df_data) > 0:
            # logger.info("update database count = %s" % len(df_data))
            field_quote = self.get_field_quote(conn)
            cur = conn.cursor()
            df_data = df_data.where(pd.notnull(df_data), None)
            df_data['UPDATE_TIME'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df_data['ETL_CRC'] = df_data['ETL_CRC'].astype(str)
            df_data['UPDATE_TIME'] = df_data['UPDATE_TIME'].astype(str)
            for i in range(len(df_data)):
                db_batch_size = 200
                row_data = df_data.iloc[i]
                row_data_where = pd.Series(
                    [row_data[value] for value in uniq_keys], index=uniq_keys)
                row_data_value = row_data.drop(uniq_keys)
                update_sql = "update %s set %s where %s " % (tablename,
                                                             ','.join([('%s%s%s = ' % (field_quote,
                                                                                       key,
                                                                                       field_quote)) +
                                                                       str('%s') for key,
                                                                                     value in
                                                                       row_data_value.iteritems()]),
                                                             ' and '.join([('%s%s%s %s ' % (field_quote,
                                                                                            key,
                                                                                            field_quote,
                                                                                            '=' if value is not None else 'is')) +
                                                                           str('%s') for key,
                                                                                         value in
                                                                           row_data_where.iteritems()]))
                tuples = self.tuple_Getter(row_data_value.append(row_data_where))
                try:
                    cur.execute(update_sql, tuples)
                    logger.debug("update %s" % row_data[uniq_keys])
                except Exception as Error:
                    logger.warning('Error: ', Error)
                if (i + 1) % db_batch_size == 0:
                    conn.commit()
                    # logger.info("update database real_count = %s" % i+1)
            conn.commit()
            cur.close()
    #
    # def merge_2_table(self, df_data, tablename, union_keys, where_condition, conn):
    #     if not type(union_keys)==list:
    #         raise ValueError("union_keys must be a list")
    #     if df_data is not None and len(df_data) > 0:
    #         df_data_db = self.get_data_from_table(tablename, union_keys, where_condition, conn)
    #
    #         # 避免与数据库中的列名关联不上的情况， 需要对主键列的类型做转换
    #         for colum_con in (df_data.dtypes[df_data.dtypes == "datetime64[ns]"].index):
    #             df_data[colum_con] = df_data[colum_con].astype(str).replace('NaT', np.nan)
    #         for colum_con in (df_data.dtypes[df_data.dtypes == "object"].index):
    #             try:
    #                 df_data[colum_con] = df_data[colum_con].astype(str)
    #             except:
    #                 pass
    #         df_data_merge = df_data.merge(
    #             df_data_db,
    #             how='left',
    #             on=union_keys,
    #             suffixes=('', '_2'),
    #             left_index=False)
    #         for colum_con in (df_data_merge.dtypes[df_data_merge.dtypes == "datetime64[ns]"].index):
    #             df_data_merge[colum_con] = df_data_merge[colum_con].astype(str).replace('NaT', np.nan)
    #
    #         df_data_insert = df_data_merge[df_data_merge['ETL_CRC_db'].astype(str) == 'nan']
    #         df_data_insert.drop(['ETL_CRC_db'], axis=1, inplace=True)
    #
    #         df_data_update = df_data_merge[(df_data_merge['ETL_CRC_db'].astype(str) != 'nan')]
    #         df_data_update = df_data_update[
    #             df_data_update['ETL_CRC'].astype(long) != df_data_update['ETL_CRC_db'].astype(long)]
    #         df_data_update.drop(['ETL_CRC_db'], axis=1, inplace=True)
    #         if df_data_insert is not None and len(df_data_insert) > 0:
    #             self.insert_2_table(tablename, df_data_insert, conn)
    #         if df_data_update is not None and len(df_data_update) > 0:
    #             self.update_2_table(tablename, df_data_update, union_keys, conn)
    #         logger.info("merge_2_table insert %s tickets, update %s tickets, %s" % (str(len(df_data_insert)),
    #                                                                             str(len(df_data_update)), where_condition))

    def merge_2_table(self, df_data, tablename, union_keys, where_condition, conn):
        if not type(union_keys)==list:
            raise ValueError("union_keys must be a list")
        if df_data is not None and len(df_data) > 0:
            df_data_db = self.get_data_from_table(tablename, union_keys, where_condition, conn)

            # 避免与数据库中的列名关联不上的情况， 需要对主键列的类型做转换
            for colum_con in (df_data.dtypes[df_data.dtypes == "datetime64[ns]"].index):
                df_data[colum_con] = df_data[colum_con].astype(str).replace('NaT', np.nan)
            for colum_con in (df_data.dtypes[df_data.dtypes == "object"].index):
                try:
                    df_data[colum_con] = df_data[colum_con].astype(str)
                except:
                    pass
            df_data_merge = df_data.merge(
                df_data_db,
                how='left',
                on=union_keys,
                suffixes=('', '_2'),
                left_index=False)
            for colum_con in (df_data_merge.dtypes[df_data_merge.dtypes == "datetime64[ns]"].index):
                df_data_merge[colum_con] = df_data_merge[colum_con].astype(str).replace('NaT', np.nan)

            # df_data_merge['CREATE_TIME'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # df_data_merge['UPDATE_TIME'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            df_data_insert = df_data_merge[df_data_merge['ETL_CRC_db'].astype(str) == 'nan']
            df_data_insert.drop(['ETL_CRC_db'], axis=1, inplace=True)

            df_data_update = df_data_merge[(df_data_merge['ETL_CRC_db'].astype(str) != 'nan')]
            df_data_update = df_data_update[
                df_data_update['ETL_CRC'].astype(long) != df_data_update['ETL_CRC_db'].astype(long)]
            df_data_update.drop(['ETL_CRC_db'], axis=1, inplace=True)
            if df_data_insert is not None and len(df_data_insert) > 0:
                self.insert_table(tablename, df_data_insert, conn)
            if df_data_update is not None and len(df_data_update) > 0:
                # df_data_update = df_data_merge.merge(data[["PI_ID"]], on="PI_ID", how="left")
                # df_data_update.drop(['ETL_CRC_db'], axis=1, inplace=True)
                self.update_2_table(tablename, df_data_update, union_keys, conn)
            logger.info("merge_2_table insert %s tickets, update %s tickets, %s" % (str(len(df_data_insert)),
                                                                                str(len(df_data_update)), where_condition))

    def merge_table(self, df_data, tablename, union_keys, where_condition, conn, db_type):
        """
        检查crc是否存在， 不存在则新插入列
        :param df_data:
        :param tablename:
        :param union_keys:
        :param where_condition:
        :param conn:
        :param db_type:  mysql vs mssql
        :return:
        """
        # df_data = df_data.iloc[1:3]
        if not type(union_keys)==list:
            raise ValueError("union_keys must be a list")
        if df_data is not None and len(df_data) > 0:

            df_data_db = self.get_data_from_table(tablename, union_keys, where_condition, conn)

            # 避免与数据库中的列名关联不上的情况， 需要对主键列的类型做转换
            for colum_con in (df_data.dtypes[df_data.dtypes == "datetime64[ns]"].index):
                df_data[colum_con] = df_data[colum_con].astype(str).replace('NaT', np.nan)
            for colum_con in (df_data.dtypes[df_data.dtypes == "object"].index):
                try:
                    df_data[colum_con] = df_data[colum_con].astype(str)
                except:
                    pass
            df_data_merge = df_data.merge(
                df_data_db,
                how='left',
                on=union_keys,
                suffixes=('', '_2'),
                left_index=False)
            for colum_con in (df_data_merge.dtypes[df_data_merge.dtypes == "datetime64[ns]"].index):
                df_data_merge[colum_con] = df_data_merge[colum_con].astype(str).replace('NaT', np.nan)

            # df_data_merge['CREATE_TIME'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # df_data_merge['UPDATE_TIME'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if "ETL_CRC" not in df_data.columns:
                df_data_merge = add_crc(
                    df_data_merge,
                    df_data_merge.columns,
                    conn,
                    tablename,
                    db_type)
                # df_data_merge["ETL_CRC"] = 1
            df_data_insert = df_data_merge[df_data_merge['ETL_CRC_db'].astype(str) == 'nan']
            df_data_insert = df_data_insert.drop(['ETL_CRC_db'], axis=1)

            df_data_update = df_data_merge[(df_data_merge['ETL_CRC_db'].astype(str) != 'nan')]
            df_data_update = df_data_update[
                df_data_update['ETL_CRC'].astype(long) != df_data_update['ETL_CRC_db'].astype(long)]
            df_data_update.drop(['ETL_CRC_db'], axis=1, inplace=True)
            if df_data_insert is not None and len(df_data_insert) > 0:
                self.insert_table(tablename, df_data_insert, union_keys, conn)
            if df_data_update is not None and len(df_data_update) > 0:
                self.update_2_table(tablename, df_data_update, union_keys, conn)
                pass
            logger.info("merge_2_table insert %s tickets, update %s tickets, %s" % (str(len(df_data_insert)),
                                                                                str(len(df_data_update)), where_condition))

    def get_data_from_table(self, tablename, arr_select_fields, where_condition, conn):
        table_lock = self.get_table_lock(conn)
        sql = """
        select
        {fields}
        ETL_CRC as ETL_CRC_db
        from {tablename} t {table_lock}
        {where_condition}
        """.format(tablename=tablename, where_condition=where_condition,
                   fields=''.join([(value + ',') for value in arr_select_fields]), table_lock=table_lock)
        # print sql
        df_return = pd.read_sql(sql, conn)
        ###1.datatime as string type compare ###
        for colum_con in (df_return.dtypes[df_return.dtypes == "datetime64[ns]"].index):
            df_return[colum_con] = df_return[colum_con].astype(str).replace('NaT', np.nan)
        for colum_con in (df_return.dtypes[df_return.dtypes == "object"].index):
            df_return[colum_con] = df_return[colum_con].astype(str)
        df_return['ETL_CRC_db'] = df_return['ETL_CRC_db'].fillna(1)
        df_return['ETL_CRC_db'] = map(lambda x: 1 if str(x) == 'None' else x, df_return['ETL_CRC_db'])
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
