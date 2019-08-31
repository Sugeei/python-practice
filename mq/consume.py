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

# 对operator做优化， 计算跟入库分开
import sys
import os
import json
import time
from datetime import datetime
import numpy as np
import pandas as pd
import sys
# from base_consensus.consensus_algo import ConsensusAlgo
# from base_consensus.data_loader import Loader
from common import add_crc as crc
from common.db_base import DB_Base
from common.logger import logger
# import multiprocessing
# from functools import wraps
# from collections import defaultdict
# from datetime import timedelta
from multiprocessing import Queue
from threading import Thread
from base_consensus.src.consen_operator import write_stk, write_schedule
from common.config import cfg
from base_consensus.src.consen_operator import statusset
from base_consensus.lib.cacheoperator import cacher
from base_consensus.src.lib import convert_score

# cfg = Config()
base = DB_Base()

this_dir = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = os.path.join(this_dir, 'consensus_config/consensus_config.json')

collection = "consensus_history"


# loader = Loader(CONFIG_PATH)

# 作为上层数据结果与dboperator的中间层。
# 从给定队列里读取数据， 再分发到不同的写库操作入口。

class Writer(Thread):
    def __init__(self, pre_date=None, queue=None, exchange=None, exqueue=None):
        Thread.__init__(self)
        Thread.setName(self, "db_writer")
        self.queue = queue
        # 表示condate
        self.pre_date = pre_date
        # self.collector = {
        #     "income": pd.DataFrame(),
        #     "tpas": pd.DataFrame(),
        # }
        self.exchange = exchange
        self.exqueue = exqueue
        # self.loader = Loader()
        # todo, 标记对数据做insert, 还是update, 特殊需求。
        # self.db_operate_type = db_operate_type
        self._stop_flag = 0

    @property
    def set_stop(self):
        self._stop_flag = 1

    @property
    def set_db_operate_type(self, type):
        self.db_operate_type = type

    def run(self):
        logger.debug("write start")
        while self._stop_flag == 0:
            # logger.debug("while true")

            try:
                channel = self.exchange.connect()
                channel.basic_consume(self.exqueue, self.callback)
                channel.start_consuming()
            except KeyboardInterrupt:
                channel.stop_consuming()
            except Exception as err:
                logger.warning("start_consuming exception %s" % err)
                # sys.exit(3)

    def callback(self, channel, method, properties, body):
        # item = self.queue.get()
        logger.info('consumed message %s ' % body)
        try:
            # print(body)
            body = body.decode('utf8')
            # body = str(body)
            item = json.loads(body)
        except Exception as err:
            item = json.loads(json.loads(body))
        # finally:
        #     logger.warning("mq callback exception %s" % err)

        self.deliver(item)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def deliver(self, item):
        curdate = item.get('date')
        status = item.get('status')
        # if status:
        # logger.info('writer get message status')
        result = cfg.mongolazy.connect().get_collection(collection).update_one({
            "date": curdate
        }, {"$set": {'status': status}})
        #
        if status == statusset.PASS:
            self.write(curdate, 'stk', write_stk)
            self.write(curdate, 'schedule', write_schedule)

    def write(self, curdate, flag, write_func):
        """

        :param curdate:
        :param flag:  stk or schedule
        :return:
        """
        ti = time.time()
        df = cacher.read_cache_df(flag, convert_score(curdate), convert_score(curdate))
        logger.info("read cache for %s time consume %s " % (flag, int(time.time() - ti)))
        # write_stk(df)
        logger.info("writer get %s df length is %s on %s" % (flag, len(df), curdate))
        if len(df) > 0:
            write_func(df)
            result = cfg.mongolazy.connect().get_collection(collection).update_one({
                "date": curdate
            }, {"$set": {flag: statusset.PASS, 'status': statusset.PASS}})
            #
            logger.info("writer done for [%s] on %s" % (flag, curdate))
        else:
            logger.info("writer length is 0 for [%s] on %s" % (flag, curdate))
            # logger.debug("write finish, exit")

    # def to_add_crc(self, data_df, target_table, uniq_keys, target_conn):
    #     # target_conn = self.loader.create_connection(conn_type='consensus_expectation_target_db')
    #     result = crc.add_crc(
    #         data_df,
    #         data_df.columns,
    #         target_conn,
    #         target_table,
    #         'mysql')
    #     result_df = result.drop_duplicates(
    #         subset=uniq_keys, keep='last').reset_index().drop(
    #         labels='index', axis=1)
    #     return result_df
    #
    # def to_update_db(self, data_df, target_table, uniq_keys, where_condition):
    #     # todo
    #     try:
    #         target_conn = self.loader.create_connection(conn_type='consensus_expectation_target_db')
    #         result_df = self.to_add_crc(data_df, target_table, uniq_keys, target_conn)
    #
    #         logger.info("operator update table:%s on %s" % (target_table, datetime.now().strftime("%Y-%m-%d "
    #                                                                                               "%H:%M:%S")))
    #         # data_df.to_csv("%s.csv" % str(time.time()))
    #         logger.debug("here to update db operator type is %s" % self.db_operate_type)
    #         if self.db_operate_type == 'insert':
    #             base.insert_2_table(
    #                 target_table,
    #                 result_df,
    #                 target_conn)
    #         elif self.db_operate_type == 'update':
    #             base.update_2_table(
    #                 target_table,
    #                 result_df,
    #                 uniq_keys,
    #                 target_conn)
    #         else:
    #             base.update(
    #                 result_df,
    #                 target_table,
    #                 uniq_keys,
    #                 where_condition,
    #                 target_conn)
    #         target_conn.close()
    #     except:
    #         logger.warning("consensus conection exception")
    #
    # def to_price_score(self, df):
    #     if df is None or len(df) == 0:
    #         return
    #     # for con_forecast_schedule
    #     con_price_score_df = df[[
    #         'code', 'pred_date', 'con_target_price', 'con_type_target_price', 'con_score',
    #         'con_type_score', 'stock_name']]
    #
    #     columns_name = [
    #         'stock_code', 'con_date', 'target_price', 'target_price_type', 'score',
    #         'score_type', 'stock_name']
    #     con_price_score_df.columns = columns_name
    #     target_table = 'con_forecast_schedule'
    #     uniq_keys = ['stock_code', 'con_date']
    #     # pred_date_s = self.pre_date.strftime("%Y-%m-%d")
    #     # where_condition = "where con_date =  '%s' " % (pred_date_s)
    #     where_condition = ""
    #     # with open('report.txt' 'a') as fh:
    #     #     df.to_csv()
    #     #     fh.write(df)
    #     #     fh.write('/n')
    #     self.to_update_db(con_price_score_df, target_table, uniq_keys, where_condition)
    #
    # def to_stock_income(self, df):
    #     if df is None or len(df) == 0:
    #         return
    #     # todo for table con_stock_income
    #     con_stock_income_df = df[[
    #         'code', 'time_year', 'pred_date', 'con_type_income', 'con_income']]
    #     columns_name = ['stock_code', 'rpt_date', 'tdate', 'income_type', 'income']
    #     con_stock_income_df.columns = columns_name
    #     target_table = 'con_stock_income'
    #     uniq_keys = ['stock_code', 'rpt_date', 'tdate']
    #     where_condition = ""
    #     # TDATE列格式转换为 20190203
    #     con_stock_income_df.loc[:, 'tdate'] = pd.to_datetime(con_stock_income_df['tdate'])
    #     con_stock_income_df.loc[:, 'tdate'] = con_stock_income_df['tdate'].dt.strftime('%Y%m%d')
    #     self.to_update_db(con_stock_income_df, target_table, uniq_keys, where_condition)
    #
    #     # TODO pandas warning
    #     con_forecast_stk_df = df[
    #         ['code', 'time_year', 'pred_date', 'con_profit', 'con_type_profit',
    #          'con_eps', 'con_type_eps', 'con_pe', 'con_net_asset', 'con_pb',
    #          'con_roe', 'stock_type', 'rpt_type', 'stock_name']]
    #     columns_name = ['stock_code', 'rpt_date', 'con_date', 'c4', 'c4_type', 'c1',
    #                     'con_type', 'c5', 'cb', 'cPB', 'c12',
    #                     'stock_type', 'rpt_type', 'stock_name']
    #     con_forecast_stk_df.columns = columns_name
    #     target_table = 'con_forecast_stk'
    #     uniq_keys = ['stock_code', 'rpt_date', 'con_date']
    #     self.to_update_db(con_forecast_stk_df, target_table, uniq_keys, where_condition)

    def distribute(self):
        for key, value in self.collector.items():
            if key == 'income':
                self.to_stock_income(value)
                # self.collector[key] = {}
            elif key == 'tpas':
                self.to_price_score(value)
            self.collector[key] = pd.DataFrame()

    def stop(self):
        self._stop_flag_event.set()


#
# 拆分任务， 按ticker算， 单独起一个线程写数据，
if __name__ == '__main__':
    pre_date = '2019-08-07'
    # # message = {"date": pre_date, "status": 'pass'}
    # message = {"date": pre_date, "schedule": pd.DataFrame()}
    # self.queue.put(message)
    # message = {"date": pre_date, "stk": ''}
    # self.queue.put(message)
    from base_consensus.lib.exchangeoperator import inform

    # income_queue = Queue()
    Writer(exchange=cfg.consensus_exchange, exqueue=cfg.consensus_queue).start()
    while True:
        # message = {"status": statusset.PASS, "message": "finish", "date": "2019-08-08"}
        message = {"status": statusset.PASS, "message": "finish", "date": int(time.time())}
        # message = 'a,b,c'
        message_str = json.dumps(message)
        inform(message)
        # inform(json.dumps(message))
        # inform(time.time())
        time.sleep(10)
    pass
