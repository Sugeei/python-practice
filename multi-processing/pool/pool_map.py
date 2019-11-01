# -*- coding: utf-8 -*-
# To collect result

import multiprocessing
import time
import logger
import random

# logger.basicConfig()
# logger = logger.getLogger("thread")
# logger.info("test")

FORMAT = "%(asctime)-15s %(clientip)s %(user)-8s %(message)s"


# logger.basicConfig(format=FORMAT)
# d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
# logger.warning("Protocol problem: %s", "connection reset")


def func(msg):
    a = int(random.uniform(0, 10))
    time.sleep(a)
    # print('******** msg %s' % str(a))
    # return a
    print('msg: ', msg)
    return 'func_return: %s' % msg


def power(i):
    i = int(i)
    return 'func_return: %s' % i ** i


if __name__ == '__main__':
    # apply_async
    # map
    # print('\n--------map------------')
    # args = [1, 2, 4, 5, 7, 8]
    # pool = multiprocessing.Pool(processes=5)
    # return_data = pool.map(func, args)
    # print('堵塞')  # 执行完func才执行该句
    # pool.close()
    # pool.join()  # join语句要放在close之后
    # print(return_data)

    # map_async
    args = list(range(10000))
    t = time.time()
    print('\n--------map_async------------')
    pool = multiprocessing.Pool(processes=5)
    result = pool.map_async(power, args)
    print('ready: ', result.ready())
    print('不堵塞')
    result.wait()  # 等待所有进程函数执行完毕

    if result.ready():  # 进程函数是否已经启动了
        if result.successful():  # 进程函数是否执行成功
            # print(result.get())
            pass# 进程函数返回值
    print("time consumed %s" % (str(time.time() - t)))
