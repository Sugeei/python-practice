# to see vesion of a module
# pandas.__version__

# 字典合并
x = {'x':1,'y':2}
y = {'a':3,'b':4}
z= {**x, **y}
print(z)

# tuple
# >>> import numpy as np
# >>> a = np.nan
# >>> tuple(a)
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# TypeError: 'float' object is not iterable
# >>> a = [np.nan]
# >>> tuple(a)
# (nan,)
# >>>


# TODO how to avoid python tuple converting np.nan to string nan
# https://stackoverflow.com/questions/14162723/replacing-pandas-or-numpy-nan-with-a-none-to-use-with-mysqldb
# TODO why df.where((pd.notnull(df)), None) is not working
# https://stackoverflow.com/questions/17534106/what-is-the-difference-between-nan-and-none
# Not-A-Number
# After years of production use [NaN] has proven, at least in my opinion, to be the best decision given the state of affairs in NumPy and Python in general. The special value NaN (Not-A-Number) is used everywhere as the NA value, and there are API functions isnull and notnull which can be used across the dtypes to detect NA values.
# ...
# Thus, I have chosen the Pythonic “practicality beats purity” approach and traded integer NA capability for a much simpler approach of using a special value in float and object arrays to denote NA, and promoting integer arrays to floating when NAs must be introduced.
# https://pandas-docs.github.io/pandas-docs-travis/user_guide/missing_data.html
# One has to be mindful that in Python (and NumPy), the nan's don’t compare equal, but None's do. Note that pandas/NumPy uses the fact that np.nan != np.nan, and treats None like np.nan.


# about pymysql insert and update, executmany, replace
# http: // www.mysqltutorial.org / mysql - replace.aspx
def update_batch(self, tablename, df_data, uniq_keys, conn, update_c_name="UPDATE_TIME"):
    """
    for loop写数据太慢， 如何batch
    http://www.mysqltutorial.org/mysql-replace.aspx
    :param tablename:
    :param df_data: pandas.DataFrame
    :param uniq_keys: no need
    :param conn:
    :param update_c_name:
    :return:
    """
    if df_data is not None and len(df_data) > 0:
        # self.logger.info("update database count = %s" % len(df_data))
        field_quote = self.get_field_quote(conn)
        cur = conn.cursor()
        df_data = df_data.where(pd.notnull(df_data), None)
        df_data[update_c_name] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # df_data['ETL_CRC'] = df_data['ETL_CRC'].astype(str)
        df_data[update_c_name] = df_data[update_c_name].astype(str)
        t1 = time.time()

        row_data = df_data.iloc[0]
        replace_sql = "REPLACE INTO %s (%s) VALUES(%s) " % (tablename,
                                                            ','.join(
                                                                [(field_quote + value + field_quote) for value in
                                                                 row_data.index.values]),
                                                            ','.join(['%s'] * len(row_data))
                                                            )
        tuples = self.tuple_convert(df_data)
        try:
            cur.executemany(replace_sql, tuples)
        except Exception as Error:
            logger.warning("update exception with table=%s, %s=%s" % (tablename, uniq_keys, list(
                row_data[uniq_keys])))
        self.logger.info("update database %s real_count = %s" % (tablename, df_data.shape[0]))
        conn.commit()
        cur.close()
        self.logger.info("update timeconsue for one ticker = %s" % int(time.time() - t1))
