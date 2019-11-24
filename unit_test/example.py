# coding=utf8
# [ read mq ] {"send_time": "2019-09-19 11:30:38", "site": "sh", "title": "\u4e2d\u56fd\u94c1\u5efa\u623f\u5730\u4ea7\u96c6\u56e2\u6709\u9650\u516c\u53f8\u516c\u5f00\u53d1\u884c2015\u5e74\u516c\u53f8\u503a\u5238(\u7b2c\u4e00\u671f)2019\u5e74\u4ed8\u606f\u516c\u544a", "redo_convert": false, "s3_key": "report/2019-09-19/20190919_1c27f7a7a56ae08fbe7ee658f96f843339b7c1fd7.pdf", "type": 0, "report_meta_id": 213766, "publish_date": "2019-09-19"}
# DEBUG:convert:[ check point ] new task report id = 213766
# DEBUG:convert:[ check point ] new task s3_address = http://cluster-s3nginx-inner.datayes-stg.com:80/pipeline//report/2019-09-19/20190919_1c27f7a7a56ae08fbe7ee658f96f843339b7c1fd7.pdf
# DEBUG:convert:[ check point ] task.get(s3_address) http://cluster-s3nginx-inner.datayes-stg.com:80/pipeline//report/2019-09-19/20190919_1c27f7a7a56ae08fbe7ee658f96f843339b7c1fd7.pdf + task.get(tool) datayes_api
# WARNING:convert:base64 taskid wrong 'str' object has no attribute 'decode'
# WARNING:convert:base64 taskid wrong 'str' object has no attribute 'decode'
# WARNING:convert:base64 taskid wrong Unicode-objects must be encoded before hashing
# INFO:convert:get_task_id e5f892e0a60308b2ccc28818268f27d4
# INFO:convert:[ formatted task ] {'processTime': 1568863838.5636585, 's3_address': 'http://cluster-s3nginx-inner.datayes-stg.com:80/pipeline//report/2019-09-19/20190919_1c27f7a7a56ae08fbe7ee658f96f843339b7c1fd7.pdf', 'redo_convert': False, 'message': '', 'reportId': 213766, 'taskId': 'e5f892e0a60308b2ccc28818268f27d4', 'tried_count': 1, 'report_type': 0, 'site': 'sh', 'title': '中国铁建房地产集团有限公司公开发行2015年公司债券(第一期)2019年付息公告', 'progress': 'undo', 'receiveTime': '2019-09-19 11:30:38', 'tool': 'datayes_api', 'publishDate': '2019-09-19', 'insertTime': '2019-09-19 11:30:38'}
# INFO:convert:mongo insert done for e5f892e0a60308b2ccc28818268f27d4
# DEBUG:convert:[ newtask ] taskid = e5f892e0a60308b2ccc28818268f27d4
import time
import unittest
import json
from util.mongohandler import MongoC
from conf.config_consul import cfg
from util.converter import Converter, PostConverter
from pdf2html_converter import task_convert

# from conf.config_boto import datayesS3_config
task = {
    u'progress': u'undo',
    u'publishDate': u'2019-09-30',
    u'redo_convert': False,
    u'reportId': 30181159,
    u'report_type': 1,
    u's3_address': u'http://cluster-s3nginx-inner.datayes.com:80/pipeline/report/2019-09-30/20190930_18e7ce71dde2fd1ce26bbd45eecf6666d36b34eac.docx',
    u'site': u'sh',
    u'taskId': u'bn_CfVjvCv3ilINZK-XUuA',
    u'title': u'\u3010\u6d77\u901a\u533b\u836f\u3011\u5fc3\u8109\u533b\u7597\u7535\u8bdd\u4f1a\u8bae\u5185\u90e820190726',
    u'tool': u'datayes_api',
    u'tried_count': 1}


# 5316052	29668719		datayes_api		done	0_dnm-UpBX4iWk_7kabVJw	0	1	1
# http://cluster-s3nginx-inner.datayes.com:80/pipeline/report/2019-05-15/20190515_184b8fa11a414d74685bf3b5146c8f1ad970ccd07.pdf
# 2019-05-15 00:00:00	股东大会-日常经营		2019-05-14 18:16:27	2019-07-02 16:50:55


class TestProcess():

    def test_pdf_url_error(self):
        task = {
            u'progress': u'undo',
            u'publishDate': u'2019-09-30',
            u'receiveTime': u'2019-09-30 08:40:13',
            u'redo_convert': False,
            u'reportId': 30181159,
            u'report_type': 1,
            u's3_address': u'http://cluster-s3nginx-inner.datayes.com:80/pipeline/report/2019-09-30/20190930_18e7ce71dde2fd1ce26bbd45eecf6666d36b34eac.docx',
            u'site': u'sh',
            u'taskId': u'bn_CfVjvCv3ilINZK-XUuA',
            u'title': u'\u3010\u6d77\u901a\u533b\u836f\u3011\u5fc3\u8109\u533b\u7597\u7535\u8bdd\u4f1a\u8bae\u5185\u90e820190726',
            u'tool': u'datayes_api',
            u'tried_count': 1}
        MongoC.remove_task(task.get("taskId"))
        MongoC.new_task(task)
        task_convert(task)
        i = 0
        status = ''
        while i < 30:
            result = MongoC.find_task('reportId', task.get('report_id'))
            if result.count() == 1:
                # break
                status = list(result)[0].get('status')
                break
            time.sleep(1)
            i += 1
        assert status == False
        # assert s3_url == cfg.s3prefix + '/' + datayesS3_config['pipeline'] + '/' + newmessage.get('s3_key')

    def test_new_task(self):
        MongoC.remove_task(task.get("taskId"))
        MongoC.new_task(task)
        # MongoC.remove_key_value('reportId', newmessage.get('report_meta_id'))
        i = 0
        rescount = 0
        while i < 120:
            result = MongoC.find_task('reportId', task.get('report_id'))
            if result.count() == 1:
                # progress = list(result)[0].get('progress')
                # if progress == 'done':
                rescount = result.count()
                break
            time.sleep(1)
            i += 1
        assert rescount == 1


if __name__ == '__main__':
    unittest.main()
