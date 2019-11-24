#


import sys
import os
import time
import traceback
from datetime import datetime
from multiprocessing import Pool
# import multiprocessing
from collections import defaultdict
from datetime import timedelta
import sys
# from pympler import asizeof
# import redis
from multiprocessing import Manager, Process
from threading import Thread


# 测试线程是否在主线程结束后退出。
# 主线程运行完之后， 子线程还会运行

class Writer(Thread):
    def __init__(self, queue, pre_date=None):
        Thread.__init__(self)
        self.queue = queue
        # 表示condate
        self.pre_date = pre_date
        self.a = 1

    def run(self):
        while self.a == 1:
            print('thread run on %s' % time.time())
            time.sleep(3)
            self.a = self.queue.get()
            print("queue get %s" % self.a)


def run_batch():
    """
    # df = tickers

    :param df:
    :param pre_date:
    :param init_data:
    :return:
    """
    incomequeue = Manager().Queue()
    Writer(incomequeue).start()

    incomequeue.put(1)
    incomequeue.put(0)
    time.sleep(1)
    print("run batch done")


if __name__ == "__main__":
    # 传参数日期，用于重跑历史， 格式：'2019-01-01'
    try:
        ds = str(sys.argv[1]).split("-")
        pre_date = datetime(int(ds[0]), int(ds[1]), int(ds[2])).date()
    except:
        pre_date = datetime.today().date()
    try:
        # 测试能扛得住多少进程
        cpucount = int(sys.argv[2])
    except:
        cpucount = 1

    this_dir = os.path.dirname(os.path.realpath(__file__))
    CONFIG_PATH = os.path.join(this_dir, 'consensus_config/consensus_config.json')

    run_batch()
