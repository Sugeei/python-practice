class DBOperator():
    def __init__(self, pool=None):
        # self.table_column_map = {}
        self.table_map = TableMap(table_column_map)
        self.dbbase = DB_Base()
        # self.pool = pool

    def insert(self, df, flag, trade_date):
        mapinfo = self.table_map.flag_map(flag)
        for key, value in mapinfo.items():
            self.record(df, trade_date, key, value)

    def insert_parallel(self, df, flag, trade_date):
        """并行"""
        """
        pool启的进程池如果写的类方法中不能正常启动， 用下面的方法可以正常启动
        """
        from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
        import multiprocessing
        all_task = []
        pool = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())
        mapinfo = self.table_map.flag_map(flag)
        for table, value in mapinfo.items():
            params = {'tablename': table, 'df': df, 'trade_date': trade_date, 'columns': value}
            future1 = pool.submit(self.record, **params)
            all_task.append(future1)
        threads_results = wait(all_task, return_when=ALL_COMPLETED)  # 主线程阻塞
        if len(threads_results[0]) > 0:
            for thread_result in threads_results[0]:
                if thread_result._exception is not None:
                    raise thread_result._exception
        if len(threads_results[1]) > 0:
            logger.error('multi insert_2_table_multi occured error')
            raise Exception('insert_2_table_multi occured error')
        pool.shutdown()

    @decorator_timecount
    def record(self, df, trade_date, tablename, columns):
        """
        根据给定的columns从df中取指定的列写入给定的表中
        :param tablename:  table name
        :param columns:  columns list to be inserted
        :return:
        """
        # DATAYES_DB = 'DYDB_MS'
        df['SECURITY_ID'] = df['SECURITY_ID'].astype(int)
        df['WINDOW'] = df['WINDOW'].astype(int)
        df['END_DATE'] = pd.to_datetime(df['END_DATE']).dt.strftime("%Y-%m-%d").astype(str)
        conn = get_db_conn_mssql(env, "FUND_PERF")
        # conn = get_db_conn_mssql('prd', "FUND_PERF")
        sub_df = df[columns]
        try:
            self.dbbase.insert_table(tablename, sub_df, conn)
            logger.info("write done date=%s, table=%s, lendgth=%s" % (trade_date, tablename, sub_df.shape[0]))
        except Exception as err:
            logger.info(
                "write exception %s date=%s, table=%s, lendgth=%s" % (err, trade_date, tablename, sub_df.shape[
                    0]))
        conn.close()
        # logger.info('date:%s rows written to db is: %s' % (trade_date, len(df_to_write)))

