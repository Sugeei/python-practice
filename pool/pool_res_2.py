# -*- coding: utf-8 -*-
# To collect result
from multipool import MultiPool
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
    # print('msg: ', msg)
    a = int(random.uniform(0, 10))
    time.sleep(a)
    print('******** msg %s' % str(a))
    return a
    # return 'func_return: %s' % msg


if __name__ == '__main__':
    # apply_async
    # map
    print('\n--------map------------')
    args = [1, 2, 4, 5, 7, 8]

    p = MultiPool()
    p.func = func
    p.data = args
    p.execute()
    print(p.result)
    # # map_async
    # print('\n--------map_async------------')
    # pool = multiprocessing.Pool(processes=5)
    # result = pool.map_async(func, args)
    # print('ready: ', result.ready())
    # print('不堵塞')
    # result.wait()  # 等待所有进程函数执行完毕
    #
    # if result.ready():  # 进程函数是否已经启动了
    #     if result.successful():  # 进程函数是否执行成功
    #         print(result.get())  # 进程函数返回值
