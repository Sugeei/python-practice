# -*- coding: utf-8 -*-

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
    print('msg: ', msg)
    time.sleep(random.uniform(99, 107))
    print('******** msg %s' % msg)
    return 'func_return: %s' % msg


if __name__ == '__main__':
    # apply_async
    print('\n--------apply_async------------')
    # pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    pool = multiprocessing.Pool(processes=2)
    results = []
    for i in range(10):
        msg = 'hello world %d' % i
        result = pool.apply_async(func, (msg,))
        results.append(result)
    print('apply_async: 不堵塞')

    for i in results:
        i.wait()  # 等待进程函数执行完毕

    for i in results:
        if i.ready():  # 进程函数是否已经启动了
            if i.successful():  # 进程函数是否执行成功
                print(i.get())  # 进程函数返回值

    # apply
    print('\n--------apply------------')
    pool = multiprocessing.Pool(processes=4)
    results = []
    for i in range(10):
        msg = 'hello world %d' % i
        result = pool.apply(func, (msg,))
        results.append(result)
    print('apply: 堵塞')  # 执行完func才执行该句
    pool.close()
    pool.join()  # join语句要放在close之后
    print(results)

    # map
    print('\n--------map------------')
    args = [1, 2, 4, 5, 7, 8]
    pool = multiprocessing.Pool(processes=5)
    return_data = pool.map(func, args)
    print('堵塞')  # 执行完func才执行该句
    pool.close()
    pool.join()  # join语句要放在close之后
    print(return_data)

    # map_async
    print('\n--------map_async------------')
    pool = multiprocessing.Pool(processes=5)
    result = pool.map_async(func, args)
    print('ready: ', result.ready())
    print('不堵塞')
    result.wait()  # 等待所有进程函数执行完毕

    if result.ready():  # 进程函数是否已经启动了
        if result.successful():  # 进程函数是否执行成功
            print(result.get())  # 进程函数返回值
