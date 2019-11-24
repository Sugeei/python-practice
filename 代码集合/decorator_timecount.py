import time


def decorator_timecount(func):
    def subfun(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        logger.info("time consumed for func %s is %s " % (func.__name__, int(time.time() - t1)))
        # print("time consumed for func %s is %s " % (func.__name__, int(time.time() - t1)))
        return result
    return subfun

