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
    print("---- finish ] %s" % task)
    # return task


class QueueConsumer(Thread):
    def __init__(self, consume_queue, i):
        Thread.__init__(self)
        Thread.setName(self, "queue_consumer %s" % i)
        self.setDaemon(True)
        self.queue = consume_queue
        self.c_id = i

    def run(self):
        while True:
            try:
                print("[ c1, start consumer %s ] %s queue length is %s" % (self.c_id, time.time(), self.queue.qsize()))

                task = self.queue.get()  # block util get task
                print("[ c2, QueueConsumer %s ] %s %s" % (self.c_id, time.time(), task))

                res = process_pool.apply_async(convert,
                                               args=(task,))  # 这个地方不会被block住，所以end_time-start_time反映的是程序执行时间

                print("[ c3, wait for task finish %s ] %s %s" % (self.c_id, time.time(), self.queue.qsize()))

                try:
                    message = res.get(timeout=30)

                except multiprocessing.TimeoutError:
                    message = "time out"

                print("[ c4 , finished ] %s" % (message))
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
                        "[ FeedQueue ] put to queue finished, %s, queue length %s" % (msg, self.queue.qsize()))
                # time.sleep(random.uniform(100, 200))
                # logger1.info("[ FeedQueue ] put taskId=%s to queue finished" % (result['taskId']))
            except:
                # logger1.error(err, exc_info=True)
                time.sleep(self.interval)


# 去掉feedqueue queueconsumer的设定
# 用下面的线程获取任务，并交给Pool处理，
# 试图用判断process_pool._taskqueue.qsize()的方式获取pool中先生队列的长度，
# 以此避免pool把所有任务吃进自己等待队列的情况， 似乎没有生效
# _cache方法测试下来靠谱
# https://stackoverflow.com/questions/5542868/python-how-can-i-check-the-number-of-pending-tasks-in-a-multiprocessing-pool

class TaskListner(Thread):
    def __init__(self):
        Thread.__init__(self)
        Thread.setName(self, "tasklistner")
        self.setDaemon(True)
        # self.queue = queue
        self.interval = 10

    def run(self):
        while True:
            try:
                print ("_taskqueue.qsize() = %s" %  len(process_pool._cache))
                # while process_pool._taskqueue.qsize() > 3:
                while len(process_pool._cache) > 3:
                    print("--------waiting *** ] ")

                    time.sleep(self.interval)
                msg = "new task %s" % time.time()
                # queue大小只有1，利用queue做多线程的调度，在mongo中处于processing状态的任务应该有『 处理进程数+1 』个
                # self.queue.put(msg)
                print("----------get msg %s" % msg)
                process_pool.apply_async(convert, args=(msg,))  # 这个地方不会被block住，所以end_time-start_time反映的是程序执行时间

                # time.sleep(1)
                # logger1.info("[ FeedQueue ] put taskId=%s to queue finished" % (result['taskId']))
            except:
                # logger1.error(err, exc_info=True)
                time.sleep(self.interval)


if __name__ == "__main__":
    max_process = int(multiprocessing.cpu_count())
    # task_queue用来传输任务
    # manager
    # task_queue = Manager().Queue(max_process)
    process_pool = Pool(processes=max_process)

    # 扫描mongo中的progress为undo的记录，put到Queue中
    # FeedQueue(task_queue).start()
    TaskListner().start()
    # Consumer进程消费该Queue的内容
    # for i in range(max_process):
    #     queueconsumer = QueueConsumer(task_queue, i).start()

    while True:
        time.sleep(10)
