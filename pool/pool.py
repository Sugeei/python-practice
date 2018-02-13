# coding:utf-8
import multiprocessing

from multiprocessing import Queue, Process, Pool, Manager
from threading import Thread
import time
import random
# from conf.logger import testlogger


def convert(task):
    print("-- convert  %s" % task)
    time.sleep(random.uniform(10, 20))
    print("[ finish ] %s" % task)
    # return task


class QueueConsumer(Thread):
    def __init__(self, consume_queue):
        Thread.__init__(self)
        Thread.setName(self, "queue_consumer")
        self.setDaemon(True)
        self.queue = consume_queue

    def run(self):
        while True:
            try:
                task = self.queue.get()  # block util get task
                print("[ QueueConsumer ] %s" % (task))

                res = process_pool.apply_async(convert,
                                               args=(task,))  # 这个地方不会被block住，所以end_time-start_time反映的是程序执行时间

                try:
                    message = res.get(timeout=30)

                except multiprocessing.TimeoutError:
                    message = "time out"

                    # print("[ finished ] %s" % (message))
            except:

                print()


class FeedQueue(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        Thread.setName(self, "FeedHtml")
        self.setDaemon(True)
        self.queue = queue
        self.interval = 10

    def run(self):
        while True:
            try:
                msg = "new task %s" % time.time()
                # queue大小只有1，利用queue做多线程的调度，在mongo中处于processing状态的任务应该有『 处理进程数+1 』个
                self.queue.put(msg)
                print(
                    "[ FeedQueue ] put to queue finished, status is %s" % (msg))
                time.sleep(random.uniform(1, 2))
                # logger1.info("[ FeedQueue ] put taskId=%s to queue finished" % (result['taskId']))
            except:
                # logger1.error(err, exc_info=True)
                time.sleep(self.interval)


if __name__ == "__main__":
    max_process = int(multiprocessing.cpu_count())
    # task_queue用来传输任务
    task_queue = Manager().Queue(2)
    process_pool = Pool(processes=2)

    # 扫描mongo中的progress为undo的记录，put到Queue中
    FeedQueue(task_queue).start()

    # Consumer进程消费该Queue的内容
    # for i in range(1):
    queueconsumer = QueueConsumer(task_queue).start()

    while True:
        time.sleep(10)
