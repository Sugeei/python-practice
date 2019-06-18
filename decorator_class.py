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

# 每两小时执行一次， 检测底层研报的更新， 发现某支股票有更新时，重新计算其一致预期值

import sys
import os
import time
import traceback
from datetime import datetime
from multiprocessing import Pool
import numpy as np
import pandas as pd
import sys
from base_consensus.consensus_algo import ConsensusAlgo
from base_consensus.data_loader import Loader
from common import add_crc as crc
from common.db_base import DB_Base
from common.logger import logger
import multiprocessing
from functools import wraps
from collections import defaultdict

base = DB_Base()

this_dir = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = os.path.join(this_dir, 'consensus_config/consensus_config.json')

loader = Loader(CONFIG_PATH)

trade_cal = loader.get_trade_cal()
tickers = loader.get_ticker()

CALGO = ConsensusAlgo()

time_consume = defaultdict(list)

#
#
# def consume(func):
#     def ret_func(*args, **kwargs):
#         t1 = time.time()
#         func(*args, **kwargs)
#         t2 = time.time()
#         time_consume[func.__name__].add(t2 - t1)
#         return t2 - t1
#
#     return ret_func()

# def consume():
#     def wrapper(f):
#         @wraps(f)
#         def wrap(self, *args, **kwargs):
#             t1 = time.time()
#             f(self, *args, **kwargs)
#             t2 = time.time()
#             time_consume[f.__name__].add(t2 - t1)
#
#         return wrap
#
#     return wrapper


class Operator(object):
    # this class is used to deal with all the three tables
    """
    一次计算所有三张表的数据，再分别写入库中
    """

    def __init__(self, ticker, datelist=None):
        self.ticker = ticker
        self.name = tickers.set_index("ticker_symbol").loc[ticker, 'SEC_SHORT_NAME']
        self.datelist = datelist
        if type(datelist) is not list:
            print("should be a date list")
        if datelist is None:
            self.datelist = [datetime.today().date()]
        self.price_score_df = None
        self.finalcial_index_df = None

    def is_trade_date(self, d):
        if d in trade_cal["TRADE_DATE"].tolist():
            return True
        return False

    def is_valid(self, d):
        # 结合delist_date检查当前要计算的 ticker, date是否合法
        delist_date = tickers.set_index('ticker_symbol').loc[self.ticker, 'delist_date']
        if delist_date is not None and d >= delist_date:
            return False
        return True
    #

    def consume(func):
        def ret_func(self, *args, **kwargs):
            t1 = time.time()
            func(self, *args, **kwargs)
            t2 = time.time()
            time_consume[func.__name__].append(t2 - t1)
            return t2 - t1

        return ret_func

    @consume
    def init_data(self, ticker):
        # to load data
        # self.trade_cal = loader.get_trade_cal() # 加载的是所有交易日，剔除了非交易日
        # 把计算三张表的数据针对某一个ticker的数据都加载进来， 再分别调用两个deal函数， 这样把两个文件合并到一个入口
        self.org_predict = loader.get_all_org_predict_fix(ticker)
        self.true = loader.get_all_true_fix(ticker)
        self.tprice_and_score = loader.get_all_tprice_and_score_fix(ticker)
        self.fiscal_pre = loader.get_all_fiscal_pre_fix(ticker)

    @consume
    def get_financial_index(self, ticker, name, pre_date):
        #
        result = CALGO.run(
            ticker,
            pre_date,
            self.org_predict,
            self.true,
            self.fiscal_pre,
            {}, 'DataYes')

        # todo 将结果返回做格式化，
        # 添加列
        result['stock_type'] = 1
        result['rpt_type'] = 4
        result['stock_name'] = name
        self.finalcial_index_df = result

    @consume
    def get_price_score_index(self, ticker, name, pre_date):
        # run_tprice_and_score
        result = CALGO.run_tprice_and_score(
            ticker,
            pre_date,
            self.tprice_and_score,
            self.org_predict,
            self.true,
            {}, 'DataYes')
        # todo 将结果返回做格式化，
        # 添加列
        result['stock_type'] = 1
        result['rpt_type'] = 4
        result['stock_name'] = name
        self.price_score_df = result

    @consume
    def format_stock_income(self, prd_date):
        # todo for table con_stock_income
        con_stock_income_df = self.finalcial_index_df[[
            'code', 'time_year', 'pred_date', 'con_type_income', 'con_income']]

        columns_name = ['stock_code', 'rpt_date', 'tdate', 'income_type', 'income']
        con_stock_income_df.columns = columns_name
        target_table = 'con_stock_income'
        uniq_keys = ['stock_code', 'rpt_date', 'tdate']
        pred_date_s = prd_date.strftime("%Y-%m-%d")
        where_condition = "where tdate =  %s " % (pred_date_s)

        # TDATE列格式转换为 20190203
        con_stock_income_df.loc[:, 'tdate'] = pd.to_datetime(con_stock_income_df['tdate'])
        con_stock_income_df.loc[:, 'tdate'] = con_stock_income_df['tdate'].dt.strftime('%Y%m%d')

        self.to_update_db(con_stock_income_df, target_table, uniq_keys, where_condition)

    @consume
    def format_price_score(self, prd_date):
        # for con_forecast_schedule
        con_price_score_df = self.price_score_df[[
            'code', 'pred_date', 'con_target_price', 'con_type_target_price', 'con_score',
            'con_type_score', 'stock_name']]

        columns_name = [
            'stock_code', 'con_date', 'target_price', 'target_price_type', 'score',
            'score_type', 'stock_name']
        con_price_score_df.columns = columns_name
        target_table = 'con_forecast_schedule'
        uniq_keys = ['stock_code', 'con_date']
        pred_date_s = prd_date.strftime("%Y-%m-%d")
        where_condition = "where con_date =  '%s' " % (pred_date_s)
        self.to_update_db(con_price_score_df, target_table, uniq_keys, where_condition)

    @consume
    def format_forecast_stk(self, prd_date):
        # todo for con_forecast_stk
        con_forecast_stk_df = self.finalcial_index_df[['code',
                                                       'time_year',
                                                       'pred_date',
                                                       'con_profit',
                                                       'con_type_profit',
                                                       'con_eps',
                                                       'con_type_eps',
                                                       'con_pe',
                                                       'con_net_asset',
                                                       'con_pb',
                                                       'con_roe',
                                                       'stock_type',
                                                       'rpt_type',
                                                       'stock_name']]
        columns_name = ['stock_code', 'rpt_date', 'con_date', 'c4', 'c4_type', 'c1',
                        'con_type', 'c5', 'cb', 'cPB', 'c12',
                        'stock_type', 'rpt_type', 'stock_name']
        con_forecast_stk_df.columns = columns_name

        target_table = 'con_forecast_stk'
        uniq_keys = ['stock_code', 'rpt_date', 'con_date']
        pred_date_s = prd_date.strftime("%Y-%m-%d")
        where_condition = "where con_date =  '%s' " % (pred_date_s)
        self.to_update_db(con_forecast_stk_df, target_table, uniq_keys, where_condition)

    @consume
    def to_add_crc(self, data_df, target_table, uniq_keys, target_conn):
        # target_conn = loader.create_connection(conn_type='consensus_expectation_target_db')
        result = crc.add_crc(
            data_df,
            data_df.columns,
            target_conn,
            target_table,
            'mysql')
        result_df = result.drop_duplicates(
            subset=uniq_keys, keep='last').reset_index().drop(
            labels='index', axis=1)
        return result_df

    @consume
    def to_update_db(self, data_df, target_table, uniq_keys, where_condition):
        # todo
        target_conn = loader.create_connection(conn_type='consensus_expectation_target_db')
        result_df = self.to_add_crc(data_df, target_table, uniq_keys, target_conn)
        base.merge_2_table(
            result_df,
            target_table,
            uniq_keys,
            where_condition,
            target_conn)
        target_conn.close()

    def run(self):
        self.init_data(self.ticker)
        for d in self.datelist:
            if not (self.is_trade_date(d) and self.is_valid(d)):
                continue
            # template for calculate
            self.get_financial_index(self.ticker, self.name, d)
            self.format_forecast_stk(d)
            self.format_stock_income(d)

            self.get_price_score_index(self.ticker, self.name, d)
            self.format_price_score(d)

# https://www.codementor.io/sheena/advanced-use-python-decorators-class-function-du107nxsv
# 拆分任务， 按ticker算， 单独起一个线程写数据，
if __name__ == '__main__':
    ticker = '000004'
    pre_date = datetime.today().date()
    consenworker = Operator(ticker, [pre_date])
    consenworker.run()

    # 543个ticker, 耗时39分钟。
    # #
    # p = Pool(processes=multiprocessing.cpu_count())
    # t1 = time.time()
    #
    # for t in tickers['ticker_symbol'].tolist():
    #     consenworker = Operator(t, [pre_date])
    #     p.apply_async(consenworker.run())
    #     # consenworker.run()
    #
    # t2 = time.time()
    # print(t2 - t1)
    # 入参ticker, date
    # todo check delist date
    # if delist_date is not None and pred_date_s >= delist_date.strftime(
    #             "%Y-%m-%d"):
    #
