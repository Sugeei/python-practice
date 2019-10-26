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
import crcmod.predefined
import time


class DB_Base():
    db_batch_size = 100

    def __init__(self, loghandler=None):
        self.logger = loghandler

    def get_type_from_table(self, tablename, conn):
        """
        从数据库中获取指定表的各列的字符类型
        For SQLserver only
        :param tablename:
        :param conn:
        :return:
        """
        sql = """
             select SO.name as t_name, SC.colid as f_id,SC.name as f_name,SC.length as f_length,SC.prec as f_prec,
             SC.scale as f_scale,ST.name as f_type from         
             sysobjects   SO, -- 对象表  
             syscolumns   SC, -- 列名表  
             systypes     ST  -- 数据类型表   
             where
             SO.name ='%s' and 
             SO.id = SC.id 
             -- and SC.id = ST.xtype
             and SC.xtype = ST.xusertype
             -- and SC.name = 'W_MAX_CONT_RISE_PERIODS'
             and SO.xtype = 'U'                   -- 类型U表示表，V表示视图  
             and SO.status >= 0    """ % tablename
        dftype = pd.read_sql(sql, conn)
        return dftype[['f_name', 'f_type']].set_index('f_name').T

    def tuple_Getter(self, x, types):
        """

        :param x:
        :param types:  dataframe.dtypes
        :return:
        """
        t = []
        for i in range(len(x)):
            if str(x[i]).lower() == 'nan' or str(x[i]).lower() == 'none':
                t.append(None)
            elif 'int' in str(types[i]):
                t.append(int(x[i]))
            elif 'decimal' in str(types[i]):
                # float
                t.append(float(x[i]))
            else:
                t.append(str(x[i]))
        return tuple(t)

    def tuple_convert_none(self, df):
        """
        TODO 有没有更好的办法处理np.nan
        将所有nan用字符None替换后，写入库的值变成了0！！！这个问题没再复现
        新的情况是以字符‘None'入库会报错
        :param df:
        :return:
        """
        # df = df.fillna('None')
        # 看上去数据库只接受空值为'None'或者NoneType, 无法识别nan
        df = df.astype(object)
        # df = df.replace('nan', 'None')
        df = df.where((pd.notnull(df)), None)
        # df.astype(object).replace(np.nan, 'None')
        tuples = [tuple(x) for x in df.values]
        return tuples

    def insert_table(self, tablename, df_data, conn):
        """

        :param tablename:
        :param df_data:
        :param conn:
        :return:
        """
        # df_data = df_data.where(pd.notnull(df_data), None)
        # TODO 获取数据表中列类型, 用来调整待入库数据的类型
        dftype = self.get_type_from_table(tablename, conn)
        dftype = dftype[df_data.columns]

        field_quote = self.get_field_quote(conn)
        cur = conn.cursor()  # <type 'pymssql.Connection'>
        insert_sql = "INSERT INTO %s (%s) VALUES(%s) " % (tablename,
                                                          ','.join(
                                                              [(field_quote + value + field_quote) for value in
                                                               df_data.columns]),
                                                          ','.join(['%s' for i in range(df_data.shape[1])]))

        for i in range(len(df_data)):
            db_batch_size = 200
            row_data = df_data.iloc[i]

            tuples = self.tuple_Getter(row_data, dftype.values[0])
            # cols = ",".join(df_data.columns)
            # sql_ins = "insert into %s(%s) values " % (tablename, cols)
            try:
                cur.execute(insert_sql, tuples)
                # cur.execute(sql_ins + '(' + ','.join(tuples) + ')')
            except Exception as Error:
                self.logger.warning("insert exception: %s %s" % (tuples, Error))
            if (i + 1) % db_batch_size == 0:
                conn.commit()
                # TODO remove
                break
                self.logger.debug("insert database %s count = %s" % (tablename, i + 1))
        conn.commit()
        self.logger.info("insert database %s real_count = %s" % (tablename, len(df_data)))
        cur.close()

    def update_batch(self, tablename, df_data, uniq_keys, conn, update_c_name="UPDATE_TIME"):
        """
        批量更新由'replace'及'executemany'实现。实际replace在做更新的时候，检测到数据库里已存在记录时，会先删除再新插入。
        这样操作主要会影响记录的inserttime. 如果对Inserttime有保留需求，可以先把inserttime取出再做上面操作。
        for loop写数据太慢， 如何batch,
        executemany 的更新速度： 7条记录/分钟，
        http://www.mysqltutorial.org/mysql-replace.aspx
        :param tablename:
        :param df_data:
        :param uniq_keys:
        :param conn:
        :param update_c_name:
        :return:
        """
        t1 = time.time()
        if df_data is not None and len(df_data) > 0:
            # self.logger.info("update database count = %s" % len(df_data))
            field_quote = self.get_field_quote(conn)
            cur = conn.cursor()
            # df_data = df_data.where(pd.notnull(df_data), None)
            df_data['ETL_CRC'] = df_data['ETL_CRC'].astype(str)
            # 设置更新时间
            df_data[update_c_name] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df_data[update_c_name] = df_data[update_c_name].astype(str)

            row_data = df_data.iloc[0]
            replace_sql = "REPLACE INTO %s (%s) VALUES(%s) " % (tablename,
                                                                ','.join(
                                                                    [(field_quote + value + field_quote) for value in
                                                                     row_data.index.values]),
                                                                ','.join(['%s'] * len(row_data))
                                                                )
            tuples = self.tuple_convert(df_data)
            # tuples = self.tuple_convert_none(df_data)
            try:
                cur.executemany(replace_sql, tuples)
            except Exception as Error:
                logger.warning("update exception with table=%s, %s=%s" % (tablename, uniq_keys, list(
                    row_data[uniq_keys])))
            self.logger.info("update database %s real_count = %s" % (tablename, df_data.shape[0]))
            conn.commit()
            cur.close()
        self.logger.info("update timeconsue for one ticker = %s ms" % int((time.time() - t1) * 1000))

    def execute_table(self, target_conn, sql, tuples):
        try:
            batch = 100
            cur = target_conn.cursor()
            if len(tuples) == 1:
                cur.execute(sql, tuples)
            elif len(tuples) > batch:
                high = batch
                while high < len(tuples):
                    cur.executemany(sql, tuples[high - batch:high])
                    high += batch
                cur.executemany(sql, tuples[high - batch: len(tuples)])
            else:
                cur.executemany(sql, tuples)

            target_conn.commit()
            cur.close()  # def insert_table_fund_label(con=target_db, tuples):
        except:  # Exception, err:
            raise ValueError
            # print err.message

    # TODO
    def update_table_batch(self, tablename, df_data, uniq_keys, conn):
        """
        写失败，也无报错 2019-03-01
        更新数据表
        将df转换成tuple, 批量处理, 批量写入
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
        df_data['ETL_CRC'] = df_data['ETL_CRC'].astype(str)
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
        # cur = conn.cursor()
        # cur.executemany(update_sql, tuples[0])
        # conn.commit()
        #
        self.execute_table(conn, update_sql, tuples)

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
        df_data['ETL_CRC'] = df_data['ETL_CRC'].astype(str)
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

    def merge_table(self, df_data, tablename, union_keys, where_condition, conn):
        if not type(union_keys) == list:
            raise ValueError("union_keys must be a list")
        if df_data is not None and len(df_data) > 0:
            df_data_db = self.get_data_from_table(tablename, union_keys, where_condition, conn)
            for column in df_data_db.columns:
                if column in df_data.columns:
                    df_data = df_data.astype({column: df_data_db[column].dtypes})
            # 避免与数据库中的列名关联不上的情况， 需要对主键列的类型做转换
            for colum_con in (df_data.dtypes[df_data.dtypes == "datetime64[ns]"].index):
                df_data[colum_con] = df_data[colum_con].astype(str).replace('NaT', np.nan)

            for colum_con in (df_data.dtypes[df_data.dtypes == "object"].index):
                try:
                    df_data[colum_con] = df_data[colum_con].astype(str)
                    # df_data = df_data.astype({colum_con: str})
                except:
                    self.logger.warning(colum_con + "failed assign type")

            # dfb = df_data_db.drop(['PMD_YEAR','PMD_QUARTER','ETL_CRC_db'], axis=1)
            # dfb = dfb.drop_duplicates()
            # df_data[df_data_db[['PMD_CITY', 'PMD_MEDICINALINFORMATIONID', 'PMD_COMPANYID',
            #                  'PMD_MEDICINALSALENUMBER']]==df_data[['PMD_CITY', 'PMD_MEDICINALINFORMATIONID',
            # #
            # # 对啊，明明有相同值，为啥merge出来为空？？？？                                             'PMD_COMPANYID',
            # ddf = df_data_db[(df_data_db["PMD_CITY"] == '北京市')
            #                  & (df_data_db["PMD_MEDICINALINFORMATIONID"] == 'D0031110200AAA0925T082')
            #                  & (df_data_db["PMD_COMPANYID"] == 'M1316')
            #                  & (df_data_db["PMD_MEDICINALSALENUMBER"] == 25788.0)]
            # #
            # test = df_data[['PMD_CITY', 'PMD_MEDICINALINFORMATIONID', 'PMD_COMPANYID', 'PMD_MEDICINALSALENUMBER']]
            # # tdf = df_data_db[['PMD_CITY', 'PMD_MEDICINALINFORMATIONID','PMD_COMPANYID', 'PMD_MEDICINALSALENUMBER']]
            # a = list(test.iloc[0])
            # df_data_merge = df_data.merge(
            #     ddf,
            #     how='left',
            #     on=['PMD_YEAR', 'PMD_QUARTER', 'PMD_CITY', 'PMD_MEDICINALINFORMATIONID', 'PMD_COMPANYID'],
            #     suffixes=('', '_2'),
            #     left_index=False)

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
                df_data_update['ETL_CRC'] != df_data_update['ETL_CRC_db']]
            df_data_update.drop(['ETL_CRC_db'], axis=1, inplace=True)
            if df_data_insert is not None and len(df_data_insert) > 0:
                self.insert_table(tablename, df_data_insert, conn)
            if df_data_update is not None and len(df_data_update) > 0:
                # df_data_update = df_data_merge.merge(data[["PI_ID"]], on="PI_ID", how="left")
                # df_data_update.drop(['ETL_CRC_db'], axis=1, inplace=True)
                self.update_2_table(tablename, df_data_update, union_keys, conn)
            self.logger.info("merge_2_table insert %s tickets, update %s tickets, %s" % (str(len(df_data_insert)),
                                                                                         str(len(df_data_update)),
                                                                                         where_condition))

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
        df_return = pd.read_sql_query(sql, conn)
        ###1.datatime as string type compare ###
        for colum_con in (df_return.dtypes[df_return.dtypes == "datetime64[ns]"].index):
            df_return[colum_con] = df_return[colum_con].astype(str).replace('NaT', np.nan)
        for colum_con in (df_return.dtypes[df_return.dtypes == "object"].index):
            df_return[colum_con] = df_return[colum_con].astype(str)
        df_return['ETL_CRC_db'] = df_return['ETL_CRC_db'].fillna(1)
        # df_return['ETL_CRC_db'] = map(lambda x: 1 if str(x) == 'None' else x, df_return['ETL_CRC_db'])
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


base = DB_Base()


def row_2_crc32(row, columns, column_type_map=None):
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
            # temp = str(row[columns[index]]) if (column_type_map is None or len(column_type_map) == 0) else value_2_str(row[columns[index]], column_type_map[columns[index]])
            temp = str(row[columns[index]])
            str_tmp += temp
            # # print type(series[columns[i]])
        # print str_tmp
        # # print series.dtype
        # return str_tmp
        return crc32(str_tmp)


def add_crc(df, fields, conn, target_table_name, conn_type):
    if conn_type == 'mssql':
        sql = """select b.name colName, c.name colType
        from sysobjects a inner join syscolumns b
        on a.id=b.id and a.xtype='U' inner join systypes c on b.xtype=c.xusertype
        where a.name='%s' and b.name in ('%s')
         AND c.name  NOT IN ('ETL_CRC') """ % (target_table_name, '\',\''.join(fields))
        column_type_map = pd.read_sql(sql, conn)
    elif conn_type == 'mysql':
        sql = """SELECT COLUMN_NAME colName ,DATA_TYPE colType
        FROM information_schema.COLUMNS
        WHERE TABLE_NAME='%s'
        and COLUMN_NAME in  ('%s')
        AND COLUMN_NAME NOT IN ('ETL_CRC') """ % (target_table_name, '\',\''.join(fields))
        column_type_map = pd.read_sql(sql, conn)
    column_type_map = column_type_map.set_index('colName').T.to_dict('list')
    try:
        df['ETL_CRC'] = df.apply(row_2_crc32, columns=fields, column_type_map=column_type_map, axis=1)
    except:
        df['ETL_CRC'] = 1
    return df


def cal_crc(df, fields, column_type_map):
    column_type_map = column_type_map.set_index('colName').T.to_dict('list')
    df['ETL_CRC'] = df.apply(row_2_crc32, columns=fields, column_type_map=column_type_map, axis=1)
    return df


def crc32(source):
    crc32 = crcmod.predefined.Crc('crc-32')
    byte_arr = bytes(source.encode('utf8'))
    crc32.update(byte_arr)
    return crc32.crcValue
