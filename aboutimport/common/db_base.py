#! usr/bin/python
# coding=utf8

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
import numpy as np
import pandas as pd
# import add_crc as crc
# import crcmod.predefined
from common.logger import logger


# import time


class DB_Base:
    db_batch_size = 100

    def __init__(self, loghandler=None):
        self.logger = loghandler or logger

    def tuple_Getter(self, x):
        for i in range(len(x)):
            # if str(type(x[i])) == "<type 'numpy.int64'>" or str(
            #         type(x[i])) == "<class 'pandas.tslib.Timestamp'>" or str(
            #     type(x[i])) == "<type 'numpy.float64'>":  # str(type(x[i])) == "<class 'numpy.int64'>":
            #     x[i] = str(x[i])  # .decode('utf-8')
            if str(x[i]).lower() == 'nan' or str(x[i]) == 'none':
                x[i] = None
            else:
                x[i] = str(x[i])  # .decode('utf-8')

        #     else:
        return tuple(x)

    def insert_batch(self, tablename, df_data, conn, insert_c_name="INSERT_TIME", update_c_name="UPDATE_TIME"):
        # print df_data
        df_data = df_data.where(pd.notnull(df_data), None)
        field_quote = self.get_field_quote(conn)
        cur = conn.cursor()  # <type 'pymssql.Connection'>
        if 'ETL_CRC' not in df_data.columns:
            df_data['ETL_CRC'] = 1
        df_data['ETL_CRC'] = df_data['ETL_CRC'].astype(str)
        df_data[insert_c_name] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df_data[update_c_name] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        datatuple = [tuple(x) for x in df_data.values]
        insert_sql = "INSERT INTO %s (%s) VALUES(%s)" % (tablename,
                                                          ','.join(
                                                              [(field_quote + value + field_quote) for value in
                                                               df_data.columns.values]),
                                                          ','.join(['%s' for i in range(len(df_data.columns.values))]))

        # 用executemany()
        try:
            cur.executemany(insert_sql, datatuple)
            # conn.commit()
        except Exception as Error:
            # print('Error: ', Error)
            self.logger.warning("insert exception: %s data=%s" % (Error, ""))

        conn.commit()
        self.logger.info("insert database real_count = %s" % (len(df_data)))
        cur.close()

    def insert_table(self, tablename, df_data, conn, insert_c_name="INSERT_TIME", update_c_name="UPDATE_TIME"):
        # print df_data
        df_data = df_data.where(pd.notnull(df_data), None)
        field_quote = self.get_field_quote(conn)
        cur = conn.cursor()  # <type 'pymssql.Connection'>
        if 'ETL_CRC' not in df_data.columns:
            df_data['ETL_CRC'] = 1
        df_data[insert_c_name] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # df_data_merge['CREATE_TIME'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df_data[update_c_name] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
            # tuples = tuple(row_data.values.tolist())
            try:
                cur.execute(insert_sql, tuples)
                cur.executemany(insert_sql, tuples)
                # conn.commit()
            except Exception as Error:
                # print('Error: ', Error)
                self.logger.warning("insert exception: %s data=%s" % (Error, tuples))
            if (i + 1) % db_batch_size == 0:
                conn.commit()
                self.logger.info("insert database count = %s" % (i + 1))
        conn.commit()
        self.logger.info("insert database real_count = %s" % (len(df_data)))
        cur.close()

    def update_table(self, tablename, df_data, uniq_keys, conn):
        """
        更新数据表
        将df转换成tuple, 批量生成tuple, 再逐条写入
        :param tablename:
        :param df_data:
        :param uniq_keys:
        :param conn:
        :return:
        """
        if df_data is None or len(df_data) == 0:
            return
        # self.logger.info("update database count = %s" % len(df_data))
        field_quote = self.get_field_quote(conn)
        # cur = conn.cursor()
        df_data = df_data.where(pd.notnull(df_data), None)
        df_data['UPDATE_TIME'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # df_data['ETL_CRC'] = df_data['ETL_CRC'].astype(str)
        df_data['UPDATE_TIME'] = df_data['UPDATE_TIME'].astype(str)
        # 转换成tuple
        # t = list(df_data.itertuples(index=False))
        # a = tuple(df_data.iloc[0])

        # 根据uniq_keys找出需要更新的列。 uniq_keys中的列作where条件。
        setcolumns = []
        for item in df_data.columns:
            if item not in uniq_keys:
                setcolumns.append(item)

        # 重新拼接df,调换列的顺序
        tuples = [tuple(row) for row in pd.concat([df_data[setcolumns], df_data[uniq_keys]], axis=1).values]
        # tuples = self.tuple_Getter(df_data[setcolumns].append(df_data[uniq_keys]))
        # tuples = self.tuple_Getter(pd.concat([df_data[setcolumns], df_data[uniq_keys]], axis=1))
        cur = conn.cursor()

        for i in range(len(tuples)):
            db_batch_size = 200
            update_sql = "update %s set %s where %s " % (tablename,
                                                         ','.join([('%s%s%s = ' % (field_quote,
                                                                                   key,
                                                                                   field_quote)) +
                                                                   str('%s') for key in setcolumns]),
                                                         ' and '.join([('%s%s%s = ' % (field_quote,
                                                                                       key,
                                                                                       field_quote)) +
                                                                       str('%s') for key in uniq_keys]))
            # debug
            # tuples = self.tuple_Getter(row_data_value.append(row_data_where))
            try:
                cur.execute(update_sql, tuples[i])
            except Exception as Error:
                print('Error: ', Error)
                # self.logger.info()
            if (i + 1) % db_batch_size == 0:
                conn.commit()
                # self.logger.info("update database real_count = %s" % i+1)
        conn.commit()
        cur.close()

    def merge_table(self, df_data, tablename, union_keys, stylename, where_condition, conn,
                    insert_c_name="CREATE_TIME"):
        if not type(union_keys) == list:
            raise ValueError("union_keys must be a list")
        if df_data is not None and len(df_data) > 0:
            df_data_db = self.get_data_from_table(tablename, union_keys + [stylename], where_condition, conn)
            for column in df_data_db.columns:
                if column in df_data.columns:
                    df_data = df_data.astype({column: df_data_db[column].dtypes})
            # 避免与数据库中的列名关联不上的情况， 需要对主键列的类型做转换
            for colum_con in (df_data.dtypes[df_data.dtypes == "datetime64[ns]"].index):
                df_data[colum_con] = df_data[colum_con].astype(str).replace('NaT', np.nan)
            for colum_con in (df_data.dtypes[df_data.dtypes == "object"].index):
                try:
                    df_data[colum_con] = df_data[colum_con].astype(str)
                except:
                    self.logger.warning(colum_con + "failed assign type")

            if len(df_data_db) == 0:
                df_data_insert = df_data
                df_data_update = pd.DataFrame()
            else:
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

                df_data_insert = df_data_merge[df_data_merge[stylename + '_2'].isnull()]
                df_data_insert.drop([stylename + '_2'], axis=1, inplace=True)

                df_data_update = df_data_merge[~df_data_merge[stylename + '_2'].isnull()]
                df_data_update = df_data_update[df_data_update[stylename] != df_data_update[stylename + '_2']]
                df_data_update.drop([stylename + '_2'], axis=1, inplace=True)

            if df_data_insert is not None and len(df_data_insert) > 0:
                self.insert_batch(tablename, df_data_insert, conn, insert_c_name)
            if df_data_update is not None and len(df_data_update) > 0:
                # df_data_update = df_data_merge.merge(data[["PI_ID"]], on="PI_ID", how="left")
                # df_data_update.drop(['ETL_CRC_db'], axis=1, inplace=True)
                self.update_table(tablename, df_data_update, union_keys, conn)
                # self.update_2_table(tablename, df_data_update, union_keys, conn)
            # self.logger.info("merge_2_table insert %s tickets, "
            #                  "update %s tickets, %s" % (str(len(df_data_insert)),
            #                                             str(len(df_data_update)),
            #                                             where_condition))

    def get_data_from_table(self, tablename, arr_select_fields, where_condition, conn):
        table_lock = self.get_table_lock(conn)
        sql = """
        select
        {fields} 
        from {tablename} t {table_lock}
        {where_condition}
        """.format(tablename=tablename, where_condition=where_condition,
                   fields=','.join(arr_select_fields), table_lock=table_lock)
        # print sql
        # sql = """
        # select
        # ticker,trade_date,convert(varchar, market_value_style)
        # from stock_factor_tags t  with (nolock)
        # where trade_date=20190730
        # """
        # TODO python3 在这里返回乱码
        df_return = pd.read_sql_query(sql, conn)
        ###1.datatime as string type compare ###
        # for colum_con in (df_return.dtypes[df_return.dtypes == "datetime64[ns]"].index):
        #     df_return[colum_con] = df_return[colum_con].astype(str).replace('NaT', np.nan)
        # for colum_con in (df_return.dtypes[df_return.dtypes == "object"].index):
        #     df_return[colum_con] = df_return[colum_con].astype(str)
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


dbbase = DB_Base()

#
# def row_2_crc32(row, columns, column_type_map=None):
#     """
#     row: 单个记录行
#     columns: 数组，行对应的列名
#     column_type_map: 字段和类型map，如：{'SECURITY_ID':'str'}，先实现这种，如果有需要自定义的转换，再实现下面这种同时，需要兼容这种参数方式
#     column_type_map: 字段和类型map，如：{'SECURITY_ID':{'field_type':'str','func':None}
#     """
#     if columns is None or len(columns) == 0:
#         return np.nan
#     else:
#         str_tmp = ''
#         for index in range(len(columns)):
#             # print index
#             # print columns[index]
#             # temp = str(row[columns[index]]) if (column_type_map is None or len(column_type_map) == 0) else value_2_str(row[columns[index]], column_type_map[columns[index]])
#             temp = str(row[columns[index]])
#             str_tmp += temp
#             # # print type(series[columns[i]])
#         # print str_tmp
#         # # print series.dtype
#         # return str_tmp
#         return crc32(str_tmp)
#
#
# def add_crc(df, fields, conn, target_table_name, conn_type):
#     if conn_type == 'mssql':
#         sql = """select b.name colName, c.name colType
#         from sysobjects a inner join syscolumns b
#         on a.id=b.id and a.xtype='U' inner join systypes c on b.xtype=c.xusertype
#         where a.name='%s' and b.name in ('%s')
#          AND c.name  NOT IN ('ETL_CRC') """ % (target_table_name, '\',\''.join(fields))
#         column_type_map = pd.read_sql(sql, conn)
#     elif conn_type == 'mysql':
#         sql = """SELECT COLUMN_NAME colName ,DATA_TYPE colType
#         FROM information_schema.COLUMNS
#         WHERE TABLE_NAME='%s'
#         and COLUMN_NAME in  ('%s')
#         AND COLUMN_NAME NOT IN ('ETL_CRC') """ % (target_table_name, '\',\''.join(fields))
#         column_type_map = pd.read_sql(sql, conn)
#     column_type_map = column_type_map.set_index('colName').T.to_dict('list')
#     try:
#         df['ETL_CRC'] = df.apply(row_2_crc32, columns=fields, column_type_map=column_type_map, axis=1)
#     except:
#         df['ETL_CRC'] = 1
#     return df
#
#
# def cal_crc(df, fields, column_type_map):
#     column_type_map = column_type_map.set_index('colName').T.to_dict('list')
#     df['ETL_CRC'] = df.apply(row_2_crc32, columns=fields, column_type_map=column_type_map, axis=1)
#     return df
#

#
# def datetime_2_str(datetime_source, format):
#     # if str(type(datetime_source)).lower() in 'datetime64':
#     # datetime_source = np.datetime64(datetime_source).astype(datetime)
#     # 设置时区
#     to_zone = tz.gettz('CST')
#     datetime_source = datetime_source.replace(tzinfo=to_zone)
#     result = datetime.strftime(datetime_source, format)  # 未发现时间偏移现象，否则这里的CST应该是个灵活的配置
#     # print result
#     return result

#
# def crc32(source):
#     crc32 = crcmod.predefined.Crc('crc-32')
#     byte_arr = bytes(source.encode('utf8'))
#     crc32.update(byte_arr)
#     return crc32.crcValue
