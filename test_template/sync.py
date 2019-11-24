# coding=utf8
# unit test
from util.taskstatus import TASKSTATUS
# /** Copyright © 2013-2016 DataYes, All Rights Reserved. */
import time
from threading import Thread
from util.mongohandler import MongoC
import unittest


class TestSync(unittest.TestCase):
    def task_init(self, task):
        MongoC.remove_task(task.get("taskId"))
        MongoC.new_task(task)

    def loopcheck(self, task, status):
        i = 0
        resstatus = ''
        while i < 60:
            result = MongoC.find_task('taskId', task.get('taskId'))
            item = result.next()

            resstatus = item.get('progress')
            if item.get('progress') == status:
                break
            time.sleep(1)
        self.assertEqual(resstatus, status)

    # def test_syncnos3key(self):
    #     # TODO 测试同步失败是否会把syncing 状态重转为‘converted'
    #     # 这种异常情况好像没法模拟
    #
    def test_syncnos3key(self):
        # uploaded -> undo with no s3key
        task = {
            "site": "sz",
            "report_type": 1,
            "publishDate": "2019-09-04",
            "reportId": 26997454,
            "tried_count": 1,
            "progress": "uploaded",
            "taskId": "2d4ecf4779549dd5403d9123b3374819",
            "s3_address": "http://cluster-s3nginx-inner.datayes-stg.com:80/pipeline/report/2019-09-04/20190904_1172d985329ddee962f5c71bfbddaae064dd0beb5.pdf",
            "title": "英唐智控:2019年面向合格投资者公开发行公司债券(第一期)2019年跟踪信用评级报告",
            "tool": "datayes_api",
            "status": True,
            "message": "",
            "s3key": "",
        }
        self.task_init(task)
        self.loopcheck(task, 'undo')

    def test_synctrue(self):
        # uploaded -> done with status = True
        task = {
            "site": "sz",
            "report_type": 1,
            "publishDate": "2019-09-04",
            "reportId": 26997454,
            "tried_count": 1,
            "progress": "uploaded",
            "taskId": "2d4ecf4779549dd5403d9123b3374819",
            "s3_address": "http://cluster-s3nginx-inner.datayes-stg.com:80/pipeline/report/2019-09-04/20190904_1172d985329ddee962f5c71bfbddaae064dd0beb5.pdf",
            "title": "英唐智控:2019年面向合格投资者公开发行公司债券(第一期)2019年跟踪信用评级报告",
            "tool": "datayes_api",
            "status": True,
            "message": "",
            "uploading": 1567738696.299,
            "s3key": "/pipeline/data_report_html_23607504d5a4b355ed3f45d49225d283.html",
            "informed": 1567591437.83211
        }
        self.task_init(task)
        self.loopcheck(task, 'done')


if __name__ == '__main__':
    unittest.main()
