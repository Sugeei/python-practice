# coding:utf-8
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
# from datetime import *
# import Queue
# import json
# import multiprocessing
# import os
# import shutil
# import subprocess
# import sys
# import time
# from decimal import Decimal, ROUND_HALF_UP
# # from threading import *
# import MySQLdb
# import pymongo
# import schedule
# from flask import Flask, request, jsonify
# from flask_restful import Resource, Api
# from pymongo import ReturnDocument
#
# # import report_env
# # import research_convert
# # import util
# import logging
# from logging.handlers import SocketHandler, DEFAULT_TCP_LOGGING_PORT
# from chinese_char_detector import ChDetector
# from conf.logger import logger
# from infrom_sender import Informer
# from converter import PostConverter
# from converter import Converter
# # from multiprocessing import Manager
# # import redis_test

logger1 = logging.getLogger()
# logger1.setLevel(logging.DEBUG)
reload(sys)
sys.setdefaultencoding('utf8')
mutex = Lock()

heart_beat = dict()
heart_beat['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
heart_beat['status'] = 1
heart_beat['message'] = "OK"

exe_location_solid = report_env.get_prop("SOLID_EXE_FILE")
exe_location_office = report_env.get_prop("OFFICE_EXE_FILE")
exchange = json.loads(report_env.get_prop("exchange"))
exchange_client = redis.Redis(host=exchange["host"], port=exchange["port"], db=0)

app = Flask(__name__)


class TaskStatus():
    SUBMIT = "undo"
    QUEUEING = "queueing"
    CONVERTING = "doing"
    FINISH = "done"


taskstatus = TaskStatus()


# 400 代表输入格式错误，或者S3访问失败，或者形成base64 md5编码id失败
class SubmitTask(Resource):
    def __init__(self):
        super(SubmitTask, self).__init__()
        global mongodb, origin_dir
        self.mongodb = mongodb
        self.origin_dir = origin_dir

    def post(self):
        task = request.get_json(force=True)
        logger1.info('get request %s' % json.dumps(task, ensure_ascii=False, encoding="utf-8"))
        if "pdf_addr" not in task.keys():
            return {'taskId': "", "status": "REFUSED", "desc": "no pdf_addr in post data"}, 400

        if "title" not in task.keys():
            return {'taskId': "", "status": "REFUSED", "desc": "no title in post data"}, 400

        report_id = task['announcement_id']
        pdf_addr = task['pdf_addr']
        title = task['title']

        tool = "solid_pdf_tool"
        if "tool" in task.keys():
            tool = task['tool']

        publish_date = datetime.strptime(time.strftime('%Y-%m-%d'), '%Y-%m-%d')
        if "publish_date" in task.keys():
            try:
                publish_date = datetime.strptime(task["publish_date"], '%Y-%m-%d')
            except Exception, err:
                logger1.error(err, exc_info=True)
                return {'taskId': "", "status": "REFUSED", "desc": "date format: 2016-01-01 "}, 400

        zsAutoCategory = None
        if "zsAutoCategory" in task.keys():
            zsAutoCategory = task['zsAutoCategory']

        doc_type = 9
        if "docType" in task.keys():
            doc_type = int(task["docType"])

        # mode 0: 之前已处理则直接返回, 1: 复用可能存在的原始HTML, 2: 复用已下载的原始文件, 9: 完全重刷
        mode = 0
        if "mode" in task.keys():
            mode = task['mode']

        if pdf_addr is None or pdf_addr == 'null':
            return {'taskId': "", "status": "REFUSED", "desc": "pdf_addr cannot be empty"}, 400

        task_id = util.base64_md5(pdf_addr + "_" + tool)
        dest_file = os.path.join(origin_dir, "%s.pdf" % task_id)
        result = self.mongodb.reports_db.solid_pdfs.find({"taskId": task_id})
        status = False
        status_msg = None
        # needDownload = 1
        if mode == 0 and result.count() > 0:
            logger1.info("taskId:%s exists, will not insert to mongo" % task_id)
            return {'taskId': task_id, "status": "ACCEPTED", "desc": ""}, 201
        elif mode in [0, 1, 2]:
            # 判断原始文件是否存在, 存在即复用, 不存在则检查s3的pdf地址是否正确
            if os.path.isfile(dest_file) is False:
                # status, status_msg = util.check_s3_file(pdf_addr)
                status, status_msg = util.get_s3_file(pdf_addr, dest_file)
            else:
                status = True
                # needDownload = 0
        else:
            # 检查s3的pdf地址是否正确
            # status, status_msg = util.check_s3_file(pdf_addr)
            status, status_msg = util.get_s3_file(pdf_addr, dest_file)
        logger1.info("download file %s , status: %s ,status message: %s " % (pdf_addr, status, status_msg))
        if status is False:
            return {'taskId': "", "status": "REFUSED", "desc": status_msg}, 400

        # 提交任务到mongo中， 置状态为 undo
        dict_hash = {
            "reportId": report_id,
            "taskId": task_id,
            "progress": taskstatus.SUBMIT,
            "pdf_address": pdf_addr,
            "submitTime": time.time(),
            "publishDate": publish_date,
            "file": "%s.pdf" % task_id,
            "title": title,
            "tool": tool,
            # "outfile": '',
            "mode": mode,
            "zsAutoCategory": zsAutoCategory,
            "docType": doc_type
            # "needDownload": needDownload
        }
        self.mongodb.reports_db.solid_pdfs.update({"taskId": task_id}, dict_hash, True, True)
        logger1.info("task submitted %s" % task_id)
        return {'taskId': task_id, "status": "ACCEPTED", "desc": ""}, 201


@app.route('/pdf2html/convert/status')
def get_report_delay():
    return jsonify(check_report_convert_status()), 200


@app.route('/pdf2html/heartbeat')
def get_heart_beat():
    global heart_beat
    result = jsonify(heart_beat)
    return result, 200


@app.route('/pdf2html/tasks/<taskId>')
def TaskResponse(taskId):
    global mongodb
    response = mongodb.reports_db.solid_pdfs.find_one({"taskId": taskId})
    logger1.info("TaskResponse: %s, %s" % (taskId, response))
    if response is None:
        return jsonify({"status": "ERROR", "output": ""}), 404
    if response['progress'] in [taskstatus.SUBMIT, taskstatus.QUEUEING, taskstatus.CONVERTING]:
        return jsonify({"status": "RUNNING", "output": ""}), 200
    elif response['progress'] == taskstatus.FINISH:
        if response['status'] != 'SUC':
            return jsonify({"status": "ERROR", "error_message": response['message'], "output": ""}), 200
        else:
            output = ''
            try:
                # status, output = util.get_remote_content(response['outfile_url'])
                with open("%s/%s_result.htm" % (dest_dir, taskId), 'r') as fhandler:
                    output = fhandler.read()
                logger1.info("TaskResponse outpus %s: %s" % (taskId, output))
                if len(output) > 0:
                    return jsonify({"status": "COMPLETED", "output": output}), 200
                else:
                    return jsonify(
                        {"status": "ERROR", "output": "", "error_message": "result file content is empty"}), 200
            except Exception, err:
                logger1.error(err, exc_info=True)
                return jsonify({"status": "ERROR", "output": "", "error_message": "error while read result file"}), 200


@app.route('/pdf2html/recentFinishedTasks')
def get_recent_finished_tasks():
    global mongodb
    try:
        cursor = mongodb.reports_db.solid_pdfs.find(
            {"progress": taskstatus.FINISH, "finishTime": {'$gt': time.time() - 600}},
            projection={"taskId": True, "status": True, "message": True, "_id": False}
        ).limit(5000).sort("finishTime", -1)
        results = []
        for document in cursor:
            if document['status'] != "SUC":
                document["error_message"] = document["message"]
            del document["message"]
            results.append(document)
            logger1.info("get_recent_finished_tasks: %s %s" % (document['taskId'], document['status']))
        count = len(results)
        return jsonify({"count": count, "results": results, "msg": ""})
    except Exception, e:
        logger1.error("Error while get recentFinishedTasks, err: %s" % e)
        return jsonify({"count": 0, "results": [], "msg": e})


def convert(task):
    # global mongodb
    dest_dir = report_env.get_prop("dest_dir")
    exe_location_solid = report_env.get_prop("SOLID_EXE_FILE")
    exe_location_office = report_env.get_prop("OFFICE_EXE_FILE")
    taskId = task["taskId"]
    pdf_file = task["pdf_path"]
    title = task["title"]
    tool = task["tool"]
    mode = task["mode"]
    zsAutoCategory = task["zsAutoCategory"]
    doc_type = task["docType"]
    status = "FAIL"
    try:
        contents = {'status': False}
        # mode 0: 之前已处理则直接返回, 1: 复用可能存在的原始HTML, 2: 复用已下载的原始文件, 9: 完全重刷
        dest_file = os.path.join(report_env.get_prop("dest_dir"), "%s.htm" % taskId)
        # 如果需要复用之前的原始HTML, 并且原始HTML存在, 则不转换调用Solid/Office
        if mode in [0, 1] and os.path.isfile(dest_file):
            logger1.info("origin html %s exists, won't be converted by solid/office again" % dest_file)
            contents = {'status': True, 'html_address': dest_file}
        else:
            # 先对pdf进行解密
            tmp_pdf_file = str(pdf_file) + "_2"
            batcmd2 = "decrypt%sqpdf --password= --decrypt %s %s" % (os.path.sep, pdf_file, tmp_pdf_file)
            logger1.info("%s" % batcmd2)
            try:
                subprocess.check_output(batcmd2, shell=True, stderr=subprocess.STDOUT, )
                shutil.move(tmp_pdf_file, pdf_file)
                logger1.info("decrypt finished for %s" % taskId)
            except Exception, err:
                logger1.error(err, exc_info=True)
                logger1.error("decrypt failed for %s, error:%s" % (taskId, err))
                if os.path.exists(tmp_pdf_file):
                    shutil.move(tmp_pdf_file, pdf_file)
            #
            # record = mongodb.reports_db.solid_pdfs.find_one({"taskId": taskId})
            # logger1.info("mongo record check (after decrypt): %s %s" % (taskId, record))

            is_pure_image_pdf = util.is_pure_image_pdf(pdf_file)
            if is_pure_image_pdf:
                logger1.warning("Refuse to convert a pure image pdf for taskId: %s, pdf: %s" % (taskId, pdf_file))
                contents = {'status': False, 'fail_message': u'Target pdf is pure image'}
            elif tool == "solid_pdf_tool":  # 使用solid进行转换
                # exe_location_solid = report_env.get_prop("SOLID_EXE_FILE")
                batcmd = '%s %s' % (exe_location_solid, pdf_file)
                # u'"./pdf2html.exe" d:/solid/origin_pdf\\16844931.pdf'
                logger1.info("solid begin to convert files, taskId:%s, cmd: %s" % (taskId, batcmd))
                try:
                    contents = subprocess.check_output(batcmd, shell=True, stderr=subprocess.STDOUT, )
                except subprocess.CalledProcessError as e:
                    raise RuntimeError(
                        "command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
                #
                # record = mongodb.reports_db.solid_pdfs.find_one({"taskId": taskId})
                # logger1.info("mongo record check (after solid): %s %s" % (taskId, record))

                contents = contents.strip().replace("\\", "/")
                contents = json.loads(contents)
                contents = util.handle_solid_contents(contents, dest_dir)
            elif "office" in tool:  # 使用office进行转换
                batcmd = '%s pdf %s FilteredHTML' % (exe_location_office, pdf_file)
                logger1.info("office begin to convert files, taskId:%s, cmd: %s" % (taskId, batcmd))
                contents = subprocess.check_output(batcmd, shell=True, stderr=subprocess.STDOUT, )
                contents = contents.strip().replace("\\", "/")
                contents = util.handle_office_contents(contents, dest_dir)

        file_path = ""
        if contents['status']:
            bad_code_detector = ChDetector(contents['html_address'])
            if bad_code_detector.ratio < 60:
                status = "FAIL"
                trans_message = "tool convert done, but with unexpected special code."
                logger1.info(
                    "Fail to convert, including special code that can not be converted correctly:%s" % (taskId))
                logger.info(
                    "Fail to convert, including special code that can not be converted correctly:%s" % (taskId))
                return status, file_path, trans_message
            else:
                if int(doc_type) == 9 or int(doc_type) == 6:
                    logger1.info("start postconverting announcement:%s" % (taskId))
                    converter = PostConverter(contents['html_address'], title, zsAutoCategory, "")
                    html = converter.run()
                    post_convert_status = converter.status
                    # file_path, post_convert_status = util.postConvert(contents['html_address'], title, zsAutoCategory)
                    if post_convert_status:
                        util.embed_image(taskId, dest_dir)
                else:
                    logger1.info("convert research report:%s" % (taskId))
                    file_path, post_convert_status = research_convert.post_convert(contents['html_address'], title,
                                                                                   zsAutoCategory)
                if post_convert_status:
                    status = "SUC"
                    logger1.info("Success to postconvert %s" % (taskId))
                    trans_message = ""
                else:
                    status = "FAIL"
                    trans_message = "tool convert done, but fail to postConvert"
                    logger1.info("Success to postconvert %s, but failed to postConvert" % (taskId))
        else:
            status = "FAIL"
            trans_message = "tool fail to convert"
            if "fail_message" in contents:
                trans_message = trans_message + ":" + contents["fail_message"]
            logger1.info("Fail to convert %s" % taskId)
        return status, file_path, trans_message

    except Exception, err:
        logger1.error(err, exc_info=True)
        message = "unknown exception: %s" % err
        return "FAIL", "", message


def pub_exchange(self, taskId, status, htmlstring, ):
    # exchange_client
    if exchange_client.ping():
        # status = exchange_client.set(self.taskId, self.htmlstring)
        # status = exchange_client.publish("html_converter", {self.taskId, self.htmlstring})
        status = exchange_client.publish("html_converter", {"status": status, "taskid": taskId,
                                                            "htmlString": htmlstring})
        self.logger.info("[ pub_exchange status=%s ] pdf=%s" % (status, taskId))
    else:
        pass


def task_convert(task):
    print ("task_convert ")
    # print ("task_convert %s" % (json.dumps(task)))
    # task = queue.get()
    # print ("get task ")
    # pdf_path = "%s/%s.pdf" % (origin_dir, task["taskId"])
    pdf_path = task.get("pdf_path")
    # task["pdf_path"] = pdf_path
    # logger.debug("-- task %s got " % pdf_path)

    # 这一段为debug用， 手动update mongo中的数据为Undo 时，有的report本地没有下载，需要先下载到本地。
    # 不再做是否下载成功的检测， 默认成功。因为在submitTask中已经做了拦截。
    if not os.path.exists(pdf_path):
        pdf_addr = task.get("pdf_address")
        util.get_s3_file(pdf_addr, pdf_path)
        # status, status_msg = util.get_s3_file(pdf_addr, pdf_path)

    task_id = task["taskId"]
    submit_time = task.get("submitTime") or time.time()
    pdf_size = os.path.getsize(pdf_path)  # bytes
    task["pdfSize"] = pdf_size
    logger.info("[ pdf size ] task = %s, %s KB" % (task_id, pdf_size / 1024))

    task_waiting_ratio = 100000
    min_waiting_time = 600

    wait_time = pdf_size / task_waiting_ratio
    if wait_time < min_waiting_time:
        wait_time = min_waiting_time
    delay_time = int(time.time() - submit_time)

    # publish_date = task.get('publishDate') or datetime.now()
    # publish_date = publish_date.strftime("%Y-%m-%d")
    pdf_s3_address = task.get('pdf_address')
    logger1.info(json.dumps(
        {"task_id": task_id, "title": task["title"], "file_size": pdf_size,
         "delay_time": delay_time,
         "wait_time": wait_time}, ensure_ascii=False))

    # category = task.get("zsAutoCategory")
    logger1.info("task = %s, origin pdf address: %s" % (task_id, pdf_s3_address))

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mongo_url = report_env.get_prop("mongo_url")
    mongodb = pymongo.MongoClient(mongo_url)
    mongodb.reports_db.solid_pdfs.update({"taskId": task_id}, {
        "$set": {"progress": taskstatus.CONVERTING, "wait_time": wait_time, "processTime": time.time(),
                 "processTimePretty": current_time,
                 "pdfSize": str(pdf_size / 1024) + " KB"}},
                                         False, False)
    # logger1.info("task = %s, origin pdf address: %s" % (task_id, pdf_s3_address))
    logger.info("[ converting ] task = %s start converting on %s" % (task['taskId'], current_time))

    dest_dir = report_env.get_prop("dest_dir")
    task["dest_dir"] = dest_dir
    task["exe_location_solid"] = exe_location_solid
    task["exe_location_office"] = exe_location_office
    logger.info("[ start validation ] task=%s" % task.get("taskId"))

    task_id, status, file_path, message, html = Converter(task).converting()
    if status:
        status = "SUC"
        message = ""
    else:
        status = "FAIL"
    if len(html) > 0:
        try:
            pub_exchange(task_id, status, html)
        except:
            pass
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mongodb.reports_db.solid_pdfs.update({"taskId": task_id}, {"$set":
                                                                   {"progress": taskstatus.FINISH,
                                                                    "finishTime": time.time(),
                                                                    "finishTimePretty": current_time,
                                                                    "status": status,
                                                                    "message": message}},
                                         True, True)
    logger.info("[ finish converting ] task = %s on %s" % (task['taskId'], current_time))
    logger.info("[ -- callback_status ] task = %s status=%s message=%s" % (task_id, status, message))


class Workers(Thread):
    def __init__(self):
        Thread.__init__(self)
        Thread.setName(self, "queue_consumer")
        self.setDaemon(True)

    def run(self):
        while True:
            for i in range(len(workers)):
                if workers[i].ready():
                    del workers[i]
                    break
            time.sleep(1)


class QueueConsumer(Thread):
    def __init__(self, consume_queue):
        Thread.__init__(self)
        Thread.setName(self, "queue_consumer")
        self.setDaemon(True)
        self.queue = consume_queue
        self.task_waiting_ratio = int(report_env.get_prop("task_waiting_ratio"))
        self.min_waiting_time = int(report_env.get_prop("min_waiting_time"))
        self.workers = []

    def run(self):
        while True:
            logger1.info("self.queue.empty() %s or len(self.workers) >= max_process %s" % (
                self.queue.empty(), len(process_pool._pool) >= max_process))
            if self.queue.empty():  # or len(process_pool._pool) >= max_process:
                time.sleep(3)
            else:
                try:
                    task = self.queue.get()
                    print ("get task %s" % task["taskId"])
                    process_pool.apply_async(task_convert, args=(task,))
                    # self.workers.append(result)
                    # process_pool.apply_async(task_convert, args=(self.queue,))
                    # logger1.info("new a task")
                except Exception, err:
                    logger1.error(err, exc_info=True)


class FeedQueue(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        Thread.setName(self, "FeedHtml")
        self.setDaemon(True)
        self.queue = queue
        self.interval = int(report_env.get_prop("scan_mongo_interval"))

    def run(self):
        while True:
            if self.queue.full():
                time.sleep(3)
            else:
                try:
                    # 优先处理最新的任务
                    result = mongodb.reports_db.solid_pdfs.find_one_and_update(
                        {"progress": taskstatus.SUBMIT},
                        {'$set': {"progress": taskstatus.QUEUEING, "processTime": time.time(), "machine": machine_ip}},
                        sort=[("publishDate", pymongo.DESCENDING), ("docType", pymongo.DESCENDING),
                              ("submitTime", pymongo.ASCENDING)],
                        return_document=ReturnDocument.BEFORE
                    )
                    if result is None:
                        logger1.info("not find undo process, sleep %s seconds" % self.interval)
                        time.sleep(self.interval)
                        continue
                    self.queue.put(result)
                    logger1.info("put taskId:%s to queue finished" % (result['taskId']))
                except Exception, err:
                    logger1.error(err, exc_info=True)
                    time.sleep(self.interval)


# 重置一小时内一直未转换成功的记录
def schedule_task():
    try:
        logger1.info("start handle schedule job")
        out_range_time_lt = time.time() - 3600
        out_range_time_gt = time.time() - 3600 * 24
        result = mongodb.reports_db.solid_pdfs.update_many(
            {"processTime": {"$lt": out_range_time_lt}, "submitTime": {"$gt": out_range_time_gt},
             "progress": {"$in": [taskstatus.CONVERTING]}},
            {"$set": {"progress": taskstatus.SUBMIT}})
        logger1.info("schedule job done, %s task(s) reset" % result.matched_count)
    except Exception, err:
        logger1.error(err, exc_info=True)


def schedule_check_heartbeat():
    logger1.info("start check heartbeat")
    global heart_beat
    if mutex.acquire():
        heart_beat['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
        heart_beat['status'] = 1
        heart_beat['message'] = "OK"
        mutex.release()
    logger1.info("end check heartbeat")


def schedule_check_report_convert_status():
    resp = check_report_convert_status()
    logger1.info("recent convert_status: %s" % json.dumps(resp))
    if resp['latest_result'] == "FAIL" or resp['today_result'] == "FAIL":
        conclusion = u""
        if resp['latest_20min_transferred'] > 0:
            conclusion = u"%s 发现%s 篇公告 html 内容20分钟内未上传,请关注调用服务问题;" % (conclusion, resp['latest_20min_transferred'])
        if resp['latest_20min_uploaded'] > 0:
            conclusion = u"%s 发现 %s 篇公告 html 已经上传， 但20分钟内未同步到 announcement，请关注调用服务或strom问题;" % (
                conclusion, resp['latest_20min_uploaded'])
        if (0 < resp['latest_all'] == resp['latest_pending']):
            conclusion = u"%s 公告长时间未转换，请关注调用服务运行情况;" % conclusion
        if resp['today_all'] > 100 and resp['today_fail_ratio'] > 0.15:
            conclusion = u"%s 大量公告转换错误或超时，请关注转换服务运行情况" % conclusion
        content = u"公告转换问题【 %s 】" % conclusion
        resp_content = json.dumps(resp)
        logger1.info(content + resp_content)
        alert_informer.send_simple_email(content + resp_content)
        alert_informer.send_wechat_msg(content)
        logger1.info(u"公告转换问题【 %s 】， 邮件及微信发送完成！" % conclusion)


def check_report_convert_status():
    period = 30
    resp = {"latest_all": 0, "latest_pending": 0, "latest_result": "SUCCESS", "today_all": 0, "today_fail": 0,
            "latest_untransferred": 0, "latest_unuploaded": 0,
            "today_fail_ratio": 0, "today_result": "SUCCESS", "period": "%smin" % period}
    if bigdata_conn is not None:
        time_format = '%Y-%m-%d %H:%M:%S'
        created_at_gt = time.strftime(time_format, time.localtime(time.time() - period * 60))
        created_at_lt = time.strftime(time_format, time.localtime(time.time() - period / 1.5 * 60))
        created_at_pending_lt = time.strftime(time_format, time.localtime(time.time() - period / 3 * 60))
        publish_date_gt = created_at_gt.split(" ")[0]
        cursor = bigdata_conn.cursor()
        cursor.execute(
            "select convert_status from report_htmls where tool='solid_pdf_tool' and publish_date >= '%s' and created_at >= '%s' and created_at <= '%s'" % (
                publish_date_gt, created_at_gt, created_at_pending_lt))
        result = cursor.fetchall()
        status_pending_list = [data[0] for data in result]
        cursor.execute(
            "select convert_status from report_htmls where tool='solid_pdf_tool' and publish_date >= '%s' and updated_at <= '%s' and convert_status in('transferred', 'uploaded')" % (
                publish_date_gt, created_at_lt))
        result = cursor.fetchall()
        status_upload_list = [data[0] for data in result]
        cursor.execute(
            "select count(1) from report_htmls where tool='solid_pdf_tool' and created_at >= '%s'" % publish_date_gt)
        today_all = int(cursor.fetchone()[0])
        cursor.execute(
            "select count(1) from report_htmls where tool='solid_pdf_tool' and created_at >= '%s' and convert_status in('failed','timeout')" % publish_date_gt)
        today_fail = int(cursor.fetchone()[0])
        bigdata_conn.commit()
        cursor.close()
        latest_all = len(status_pending_list)
        latest_pending = status_pending_list.count('pending')
        latest_20min_transferred = status_upload_list.count('transferred')
        latest_20min_uploaded = status_upload_list.count('uploaded')
        latest_result = "FAIL" if (0 < latest_all == latest_pending) or (
                len(status_upload_list) > 0) else "SUCCESS"
        fail_ratio = float(today_fail) / today_all
        today_result = "FAIL" if (today_all > 100 and fail_ratio > 0.15) else "SUCCESS"
        resp = {"latest_all": latest_all, "latest_pending": latest_pending, "latest_result": latest_result,
                "latest_20min_transferred": latest_20min_transferred, "latest_20min_uploaded": latest_20min_uploaded,
                "today_all": today_all, "today_fail_ratio": round(fail_ratio, 2), "today_fail": today_fail,
                "today_result": today_result, "period": "%smin" % period}
    return resp


def schedule_clear_files():
    try:
        logger1.info('start to clear history files %s seconds ago' % history_file_save_period)
        last_modify_time = time.time() - int(history_file_save_period)
        rm_dir_beyond_time(origin_dir, last_modify_time)
        rm_dir_beyond_time(dest_dir, last_modify_time)
    except Exception, err:
        logger1.error(err, exc_info=True)
        # print


def rm_dir_beyond_time(dir, time):
    logger1.info("start to clear dir: %s" % dir)
    for each_file in os.listdir(dir):
        ft = os.stat(dir + "/" + each_file)
        file_time = int(ft.st_mtime)
        if file_time < time:
            if os.path.isfile(dir + "/" + each_file):
                logger1.info("rm file: %s" % each_file)
                os.remove(dir + "/" + each_file)
            elif os.path.isdir(dir + "/" + each_file):
                logger1.info("rm dir: %s" % each_file)
                shutil.rmtree(dir + "/" + each_file)


def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)


def get_local_ip():
    import socket
    hostname = socket.gethostname()
    ret = socket.gethostbyname(hostname)
    # print ret
    return ret


class MysqlConn(object):
    def __init__(self, config_json_str):
        self.mysql_config = json.loads(config_json_str, encoding='utf-8')

    def connect(self):
        mysql_conn = MySQLdb.connect(**self.mysql_config)
        logger.info("mysql connection creation with config = %s" % self.mysql_config)
        return mysql_conn


if __name__ == "__main__":
    '''
    # 同时只能运行一个转换服务
    from win32event import CreateMutex
    from win32api import GetLastError
    from winerror import ERROR_ALREADY_EXISTS

    handle = CreateMutex(None, 1, 'converter service based on solid')
    if GetLastError() == ERROR_ALREADY_EXISTS:
        print 'service is already running, exist'
        time.sleep(3)
        sys.exit(1)
    '''
    # 启动监听日志的service
    import networklogging

    log_server = multiprocessing.Process(name='logserver', target=networklogging.main)
    log_server.daemon = True
    log_server.start()

    global workers, origin_dir, mongodb, process_pool, history_file_save_period, dest_dir, machine_ip, alert_informer, bigdata_conn
    bigdata_conn = MysqlConn(report_env.get_prop("bigdata_conn")).connect()
    alert_informer = Informer(json.loads(report_env.get_prop("mail_source"), "utf-8"),
                              json.loads(report_env.get_prop("mail_target"), "utf-8"))
    machine_ip = get_local_ip()
    report_env.init_config()
    history_file_save_period = report_env.get_prop("history_file_save_period")
    mongo_url = report_env.get_prop("mongo_url")
    mongodb = pymongo.MongoClient(mongo_url)
    workers = []
    origin_dir = report_env.get_prop("origin_dir")

    if not os.path.exists(origin_dir):
        os.mkdir(origin_dir)

    dest_dir = report_env.get_prop("dest_dir")
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    max_process = int(report_env.get_prop("max_process"))
    print ("max_process:" + str(max_process))
    # task_queue用来传输任务
    # task_queue = Queue.Queue(1)
    task_queue = Manager().Queue(max_process)
    process_pool = multiprocessing.Pool(processes=max_process)

    # 扫描mongo中的progress为undo的记录，put到Queue中
    FeedQueue(task_queue).start()

    # Consumer进程消费该Queue的内容
    # for i in range(max_process):
    for i in range(1):
        QueueConsumer(task_queue).start()
        # Workers().start()

    # 定时任务
    schedule.every(15).minutes.do(schedule_task)
    schedule.every(5).minutes.do(schedule_check_heartbeat)
    schedule.every(5).minutes.do(schedule_check_report_convert_status)
    schedule.every().day.at("01:30").do(schedule_clear_files)

    schedule_thread = Thread(target=run_schedule)
    schedule_thread.start()

    # 启动flask server 监听用户请求
    print 'start web server'

    while True:
        try:
            api = Api(app)
            try:
                api.add_resource(SubmitTask, "/pdf2html/tasks")
            except Exception, err:
                logger1.error(err, exc_info=True)
            app.run(host="0.0.0.0", port=9090, debug=False)
        except Exception, err:
            logger1.error(err, exc_info=True)
