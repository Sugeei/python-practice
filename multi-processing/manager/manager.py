from multiprocessing import Process, Manager


def f(d, l):
    d[1] = '1'
    d['2'] = 2
    d[0.25] = None
    l.reverse()


class Demo():
    def __init__(self, m):
        self.data = m
        pass

    def get(self, key):
        if key not in self.data.keys():
            self.data[key] = 3
        else:
            print(self.data.get(key))


def fun(demo, key):
    print(demo.get(key))


def main(demo):
    from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
    import multiprocessing

    all_task = []
    pool = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())
    # mapinfo = self.table_map.flag_map(flag)
    for i in ['a', 'c', 'b']:

        params = {'demo': demo, 'key': i}
        future1 = pool.submit(fun, **params)
        all_task.append(future1)
        threads_results = wait(all_task, return_when=ALL_COMPLETED)  # 主线程阻塞
        if len(threads_results[0]) > 0:
            for thread_result in threads_results[0]:
                if thread_result._exception is not None:
                    raise thread_result._exception
        if len(threads_results[1]) > 0:
            # logger.error('multi insert_2_table_multi occured error')
            raise Exception('insert_2_table_multi occured error')
    pool.shutdown()


if __name__ == '__main__':
    # manager cannot be global variable
    manager = Manager()

    d = manager.dict()
    d['a'] = 0
    d['b'] = 1

    demo = Demo(d)
    main(demo)
    # p1 = Process(target=main, args=(demo, 'a'))
    # p2 = Process(target=main, args=(demo, 'c'))
    #
    # # l = manager.list(range(10))
    #
    # # p = Process(target=f, args=(d, l))
    # p1.start()
    # p2.join()

    print(d)

    # print d
    # print l

# can python manager be shared among different processes
