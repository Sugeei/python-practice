# coding:utf-8
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool


#
# mutex = Lock()
#
#
# def res_collect(func):
#     def func_wrapper(data, result):
#         if mutex.acquire():
#             result.append(func(data))
#             mutex.release()
#         return result
#
#     return func_wrapper


class MultiPool(object):

    def __init__(self, func=None, data=None):
        self.func = func
        self.data = data
        self.result = []
        self.process_pool = ThreadPool(
            processes=multiprocessing.cpu_count() - 1)

    @property
    def set_func(self, func):
        self.func = func

    @property
    def set_data(self, data):
        self.data = data

    @property
    def get_result(self):
        return self.result

    def execute(self):
        self.result = self.process_pool.map(self.func, self.data)
        self.process_pool.close()
        self.process_pool.join()
