# coding:utf8
# /**
# * 通联数据机密
#  * --------------------------------------------------------------------
#  * 通联数据股份公司版权所有 © 2013-1016
#  *
#  * 注意：本文所载所有信息均属于通联数据股份公司资产。本文所包含的知识和技术概念均属于
#  * 通联数据产权，并可能由中国、美国和其他国家专利或申请中的专利所覆盖，并受商业秘密或
#  * 版权法保护。
#  * 除非事先获得通联数据股份公司书面许可，严禁传播文中信息或复制本材料。
#  *
#  * DataYes CONFIDENTIAL
#  * --------------------------------------------------------------------
#  * Copyright © 2013-2016 DataYes, All Rights Reserved.
#  *
#  * NOTICE:  All information contained herein is the property of DataYes
#  * Incorporated. The intellectual and technical concepts contained herein are
#  * proprietary to DataYes Incorporated, and may be covered by China, U.S. and
#  * Other Countries Patents, patents in process, and are protected by trade
#  * secret or copyright law.
#  * Dissemination of this information or reproduction of this material is
#  * strictly forbidden unless prior written permission is obtained from DataYes.
#  */
#
# /** Copyright © 2013-2016 DataYes, All Rights Reserved. */
import time
from threading import Thread
import pandas as pd
from pymongo import ReturnDocument
from conf.config_consul import cfg, mcollection, mongodb
from conf.logger import logger
from taskstatus import TASKSTATUS
# from conf.config_consul import Config
from datetime import datetime, timedelta
from db_base import DB_Base
from mongohandler import MongoC
from monitor import add_heartbeat

# cfg = Config()

status = True


# 同步all
class Sync(Thread):
    """
        Search for 'informed' tasks, update database
        """

    def __init__(self):
        Thread.__init__(self)
        Thread.setName(self, "SyncStatus")
        self.setDaemon(True)
        self.interval = 3600
        self.timestamp = datetime.now()

    def run(self):
        while True:
            # try:
            result = mongodb.get_collection(mcollection).find(
                {"insertTime": {"$gte": (datetime.today() - timedelta(seconds=self.interval + 1)).strftime("%Y-%m-%d")}
                 },
                {"reportId": 1, "title": 1, "tool": 1,
                 "progress": 1, "taskId": 1, "report_type": 1,
                 "s3_address": 1, "publishDate": 1},
            )
            logger.info("[ sync_all ] run on %s" % time.time())
            logger.info("[ sync_all ] run on %s, task length is %s" % (time.time(), len(list(result))))

            self.update_db(list(result))
            time.sleep(self.interval)

    def update_db(self, data):
        if data is None or len(data) == 0:
            return
        df_data = pd.DataFrame([data], columns=data.keys())
        data['pre_status'] = data['progress']
        df_data = df_data[['reportId', 'title', 'tool', 'progress', 'taskId', 'report_type',
                           's3_address', 'publishDate']]
        df_data.columns = ['report_id', 'title', 'tool', 'convert_status', 'convert_task_id',
                           'report_type', 'absolute_pdf_s3_url', 'publish_date']
        dbbase = DB_Base()
        try:
            dbbase.update(df_data, "report_htmls", ['report_id', 'tool'], """where report_id=%s""" % data["reportId"],
                          cfg.bigdatadb.connect())
        except Exception as err:
            add_heartbeat({
                "name": "sync_batch_exception"  # which means found in reporthtmls but not found in mongo
            })


# 只同步uploaded
class SyncStatus(Thread):
    """
        Search for 'informed' tasks, update database
        """

    def __init__(self):
        Thread.__init__(self)
        Thread.setName(self, "SyncStatus")
        self.setDaemon(True)
        self.interval = 30
        self.timestamp = datetime.now()

    def run(self):
        while True:
            try:
                result = mongodb.get_collection(mcollection).find_one_and_update(
                    {"progress": {"$in": [TASKSTATUS.FINISH, TASKSTATUS.PASSUP]}
                     # {"progress": TASKSTATUS.PASSUP,
                     },
                    {'$set': {
                        "progress": TASKSTATUS.RECORD,  # to indicate syncing
                        "processTime": time.time(),
                    }},
                    {"reportId": 1, "title": 1, "tool": 1, "s3key": 1,
                     "status": 1, "tried_count": 1,
                     "progress": 1, "taskId": 1, "pdfSize": 1, "report_type": 1,
                     "s3_address": 1, "publishDate": 1, "message": 1},
                    # sort=[("publishDate", pymongo.DESCENDING)
                    #       ("submitTime", pymongo.ASCENDING)],
                    return_document=ReturnDocument.BEFORE
                )
                if result is None:
                    logger.info("[ syncStatus ] sleep %s seconds" % self.interval)
                    time.sleep(self.interval)
                    continue
                self.update_db(result)
            except Exception as err:
                # status = False
                logger.warning("sync exception %s" % err)
                exit(1)

    def sync_all(self):
        result = mongodb.get_collection(mcollection).find(
            {"insertTime": {"$gte": (datetime.today() - timedelta(seconds=self.interval + 1)).strftime("%Y-%m-%d")}
             },
            {"reportId": 1, "title": 1, "tool": 1,
             "progress": 1, "taskId": 1, "report_type": 1,
             "s3_address": 1, "publishDate": 1},
        )
        logger.info("[ sync_all ] run on %s" % time.time())
        logger.info("[ sync_all ] run on %s, task length is %s" % (time.time(), len(list(result))))

        self.update_all(list(result))
        time.sleep(self.interval)

    def update_all(self, data):

        if data is None or len(data) == 0:
            return
        df_data = pd.DataFrame([data], columns=data.keys())
        data['pre_status'] = data['progress']
        df_data = df_data[['reportId', 'title', 'tool', 'progress', 'taskId', 'report_type',
                           's3_address', 'publishDate']]
        df_data.columns = ['report_id', 'title', 'tool', 'convert_status', 'convert_task_id',
                           'report_type', 'absolute_pdf_s3_url', 'publish_date']
        dbbase = DB_Base()
        try:
            dbbase.update(df_data, "report_htmls", ['report_id', 'tool'],
                          """where report_id=%s""" % data["reportId"],
                          cfg.bigdatadb.connect())
        except Exception as err:
            add_heartbeat({
                "name": "sync_batch_exception"  # which means found in reporthtmls but not found in mongo
            })

    def sync_mongo(self):
        # 查询report_htmls中的状态，如果为done, 则同步回mongo
        # 这个暂不运行， 如果考虑下游状态的话， 将mongo中的informed任务同步到report htmls表时不直接改状态为done,
        # 需要等表中状态变成done的时候再更新mongo
        logger.debug("[ sync_mongo loop to get a task in status %s ]" % (TASKSTATUS.DONE))
        df_data = self.get_db()

        for taskid in list(df_data["convert_task_id"].values):
            result = mongodb.get_collection(mcollection).find_one_and_update(
                {"taskId": taskid,
                 },
                {'$set': {
                    "progress": TASKSTATUS.DONE,
                    "processTime": time.time(),
                }},
                {"reportId": 1, "title": 1, "tool": 1, "s3key": 1,
                 "progress": 1, "taskId": 1, "pdfSize": 1, "report_type": 1,
                 "s3_address": 1, "publishDate": 1, "message": 1},
                # sort=[("publishDate", pymongo.DESCENDING)
                #       ("submitTime", pymongo.ASCENDING)],
                return_document=ReturnDocument.BEFORE
            )

    def sync_db(self):
        # 将mongo 中状态为informed的记录同步到report_htmls
        # 通知发出就将状态置为done了， 这里没有等下游确认， 无状态操作， 不关心下游什么时候改记录状态为done
        # logger.info("[ SyncStatys loop to get a task in status %s ]" % (TASKSTATUS.INFORMED))
        try:
            result = mongodb.get_collection(mcollection).find_one_and_update(
                {"progress": {"$in": [TASKSTATUS.FINISH, TASKSTATUS.PASSUP]}
                 # {"progress": TASKSTATUS.PASSUP,
                 # "status": True
                 },
                {'$set': {
                    "progress": TASKSTATUS.RECORD,  # to indicate syncing
                    "processTime": time.time(),
                }},
                {"reportId": 1, "title": 1, "tool": 1, "s3key": 1,
                 "status": 1, "tried_count": 1,
                 "progress": 1, "taskId": 1, "pdfSize": 1, "report_type": 1,
                 "s3_address": 1, "publishDate": 1, "message": 1},
                # sort=[("publishDate", pymongo.DESCENDING)
                #       ("submitTime", pymongo.ASCENDING)],
                return_document=ReturnDocument.BEFORE
            )
        except KeyError as err:
            logger.warning("sync_db exception %s" % err)
        except Exception as err:
            # TODO to get record in mongo which raise error
            logger.warning("sync_db upknown exception %s " % err)

        # insert or update, all set

        if result is None:
            logger.info("[ syncStatus ] sleep %s seconds" % self.interval)
            time.sleep(self.interval)
            return
        # result['progress'] = TASKSTATUS.FINISH
        self.update_db(result)
        # logger.info("[ syncStatus done to report htmls db ] %s" % result["taskId"])

    def sync_status(self):
        # 将mongo 中状态为informed的记录同步到report_htmls
        # 通知发出就将状态置为done了， 这里没有等下游确认， 无状态操作， 不关心下游什么时候改记录状态为done
        # logger.info("[ SyncStatys loop to get a task in status %s ]" % (TASKSTATUS.INFORMED))
        # result = mongodb.get_collection(mcollection).find({'progress': TASKSTATUS.INFORMED})
        try:
            result = mongodb.get_collection(mcollection).find_one_and_update(
                {"progress": {"$in": [TASKSTATUS.FINISH, TASKSTATUS.PASSUP]}
                 # {"progress": TASKSTATUS.PASSUP,
                 # "status": True
                 },
                {'$set': {
                    "progress": TASKSTATUS.SYNC,
                    "processTime": time.time(),
                }},
                {"reportId": 1, "title": 1, "tool": 1, "s3key": 1,
                 "status": 1, "tried_count": 1,
                 "progress": 1, "taskId": 1, "pdfSize": 1, "report_type": 1,
                 "s3_address": 1, "publishDate": 1, "message": 1},
                # sort=[("publishDate", pymongo.DESCENDING)
                #       ("submitTime", pymongo.ASCENDING)],
                return_document=ReturnDocument.BEFORE
            )
        except KeyError as err:
            logger.warning("sync_db exception %s" % err)
        except Exception as err:
            # TODO to get record in mongo which raise error
            logger.warning("sync_db upknown exception %s " % err)

        # insert or update, all set

        if result is None:
            logger.info("[ syncStatus ] sleep %s seconds" % self.interval)
            time.sleep(self.interval)
            return
        # result['progress'] = TASKSTATUS.FINISH
        self.update_db(result)
        logger.info("[ syncStatus done to report htmls db ] %s" % result["taskId"])

    def update_db(self, data):
        if data is None or len(data) == 0:
            return
        df_data = pd.DataFrame([data], columns=data.keys())

        if 'tried_count' not in df_data.columns:
            df_data["tried_count"] = 1
        if "s3key" not in df_data.columns:
            logger.warning("syndb get result with no s3key, back undo %s " % data["taskId"])
            return

        data['pre_status'] = data['progress']
        df_data = df_data[['reportId', 'title', 'tool', 's3key', 'progress', 'taskId', 'report_type',
                           's3_address', 'publishDate', 'message', 'tried_count']]
        df_data.columns = ['report_id', 'title', 'tool', 'html_s3_url', 'convert_status', 'convert_task_id',
                           'report_type', 'absolute_pdf_s3_url', 'publish_date', 'error_reason', 'tried_counts']

        df_data['convert_status'] = df_data['convert_status'].apply(
            lambda x: TASKSTATUS.FAIL if x == TASKSTATUS.PASSUP else TASKSTATUS.FINISH)
        dbbase = DB_Base()
        try:
            # logger.debug("[[ update_db run ]]")
            dbbase.update(df_data, "report_htmls", ['report_id', 'tool'], """where report_id=%s""" % data["reportId"],
                          cfg.bigdatadb.connect())
            logger.info("[ update_db done with %s ]" % data.get("taskId"))
            MongoC.update(data.get("taskId"), "progress", TASKSTATUS.SYNC)

        except Exception as err:
            # TODO with exception, reset mongo status, and sleep
            add_heartbeat({
                "name": "sync_todb_exception"  # which means found in reporthtmls but not found in mongo
            })
            logger.warning("sync to report html exception %s %s, set back status = %s" % (
                data["taskId"], err, data.get('pre_status')))
            MongoC.update(data.get("taskId"), "progress", data.get('pre_status'))
            time.sleep(60)

    def get_db(self):
        # 从report htmls表中找出状态为done的记录
        sql = """select report_id, convert_task_id from bigdata.report_htmls where convert_status='%s' and 
            updated_at>'%s' """ % (
            TASKSTATUS.DONE,
            self.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        df_data = pd.read_sql_query(sql, cfg.bigdatadb.connect())

        return df_data


# TODO 添加监听report_htmls表的状态变化， 获取到后更新mongo, 用于触发发送给下游的消息。

if __name__ == "__main__":
    #
    # #
    # 接入新任务
    # taskreceiver = NewTask(source_msg_exchange, source_msg_queue)
    # taskreceiver.start()
    # #
    # 转换任务
    # TaskListner().start()
    #
    # TODO 转换失败的任务批量将状态置为done
    # 上传完成后将uploaded状态同步到数据库
    # S3Uploader().start()
    #
    # # 将mongo 中所有状态为uploaded同步到report_html
    # Sync().start()
    SyncStatus().start()
    #
    # # to 通知下游 uploaded -> informed
    # Informer(inform_mq_conn, inform_msg_queue).start()
    #
    # # # 监听重转任务
    # dbsync = DBSync(bigdata_db)
    # dbsync.start()

    while True:
        time.sleep(100)

    # TODO
    # 1.开通访问国信s3端口443
    # 2.report_htmls访问权限
    # 3.datayes S3 bucket=pipeline开通访问权限
