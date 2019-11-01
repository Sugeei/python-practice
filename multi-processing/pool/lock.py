# -*- coding: utf-8 -*-

from multiprocessing import Process, Lock
import os, time, datetime, random


def task_1(lock, name):
    while True:
        lock.acquire()
        print('Run task_1 %s (%s)...' % (name, os.getpid()))
        lock.release()
        time.sleep(random.randint(5, 10))
        print('id = %s over at %s' % (name, datetime.datetime.now()))


if __name__ == '__main__':
    print('[ start ] Parent process pid is %s. Start at %s' % (os.getpid(), datetime.datetime.now()))
    lock = Lock()
    ps = []
    for i in range(5):
        p = Process(target=task_1, args=(lock, i))
        p.start()
        ps.append(p)

    # join 用将主进程卡住， 等待子进程执行完成
    # 当执行下面的join语句时， 最后"[ end ] "在子进程结束前不会执行
    # 当注释下面join语句， "[ end ] "会在"[ start ]"后打印出来。 主进程退出， 留下子进程执行。
    for p in ps:
        p.join()

    print('[ end ] Parent process done at %s' % datetime.datetime.now())
