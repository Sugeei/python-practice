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
# import pandas as pd
import sys
# from pymongo import ReturnDocument
# from conf.config_consul import cfg, mcollection, mongodb
# from conf.logger import logger
# from taskstatus import TASKSTATUS
# # from conf.config_consul import Config
from datetime import datetime, timedelta

# from db_base import DB_Base
# from mongohandler import MongoC
# from monitor import add_heartbeat

# cfg = Config()

status = True


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
        i = 0
        while True:
            try:
                i += 1
                print(i)
                time.sleep(1)
                if i == 300:
                    raise ValueError
            except Exception as err:
                # status = False
                print("sync exception %s" % err)
                sys.exit(1)


# TODO 添加监听report_htmls表的状态变化， 获取到后更新mongo, 用于触发发送给下游的消息。

if __name__ == "__main__":
    # ed同步到report_html
    # Sync().start()
    # SyncStatus().start()
    #
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
            sys.exit(1)
    # # to 通知下游 uploaded -> info
    # while True:
    #     time.sleep(100)

    print('exit')
    # TODO
    # 1.开通访问国信s3端口443
    # 2.report_htmls访问权限
    # 3.datayes S3 bucket=pipeline开通访问权限
