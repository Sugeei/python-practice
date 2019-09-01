# coding:utf8
import time
from threading import Thread
import sys
from datetime import datetime, timedelta

status = True



# 只同步uploaded
class SyncStatus(Thread):
    """
        """

    def __init__(self):
        Thread.__init__(self)
        Thread.setName(self, "SyncStatus")
        self.setDaemon(True)
        self.interval = 30
        self.timestamp = datetime.now()

    def run(self):
        i = 0
        while True:
            try:
                i += 1
                print(i)
                time.sleep(1)
                if i == 3:
                    raise ValueError
            except Exception as err:
                # status = False
                print("sync exception %s" % err)
                # sys.exit(1) # can exit main.py
                exit(2) # can exit main.py


if __name__ == "__main__":
    SyncStatus().start()
    while True:
        time.sleep(100)

    print('exit') # will not be executed
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



if __name__ == "__main__":
    #
    # #
    SyncStatus().start()
    #
    # # to
    while True:
        time.sleep(100)

