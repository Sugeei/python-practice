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
