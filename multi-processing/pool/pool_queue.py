# coding=utf8
# https://stackoverflow.com/questions/55643339/python-multiprocessing-sharing-data-between-processes
# https://stackoverflow.com/questions/48162230/how-to-share-data-between-all-process-in-python-multiprocessing
# Since processes are independent and don't share the same memory space, they are appending correctly but its appending to its own self.all_nums_list for each process.
import multiprocessing as mp

from multiprocessing import Process, Queue
from threading import Thread
import time
import pandas


def foo(q):
    q.put('hello')


class Reader(Thread):
    def __init__(self, queue, pre_date=None):
        Thread.__init__(self)
        self.queue = queue
        self.pre_date = pre_date
        # self.loader = Loader()

    def run(self):
        while True:
            self.queue.put(int(time.time()))
            self.queue.put(pandas.DataFrame([1, 2, 3]))
            time.sleep(3)


class Writer(Thread):
    def __init__(self, queue, pre_date=None):
        Thread.__init__(self)
        self.queue = queue
        self.pre_date = pre_date
        # self.loader = Loader()

    def run(self):
        while True:
            print("get", self.queue.get())


if __name__ == '__main__':
    # ctx = mp.get_context('spawn')
    q = Queue()
    Reader(q).start()
    Writer(q).start()
#
# def add_process(queue, numbers_to_add):
#     for number in numbers_to_add:
#         queue.put(number)
#
#
# class AllNumsClass:
#     def __init__(self):
#         self.queue = mp.Queue()
#
#     def get_queue(self):
#         return self.queue
#
#
# if __name__ == '__main__':
#
#     all_nums_class = AllNumsClass()
#
#     processes = []
#     p1 = mp.Process(target=add_process, args=(all_nums_class.get_queue(), [1, 3, 5]))
#     p2 = mp.Process(target=add_process, args=(all_nums_class.get_queue(), [2, 4, 6]))
#
#     processes.append(p1)
#     processes.append(p2)
#     for p in processes:
#         p.start()
#     for p in processes:
#         p.join()
#
#     output = []
#     while all_nums_class.get_queue().qsize() > 0:
#         output.append(all_nums_class.get_queue().get())
#     print(output)
