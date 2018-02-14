import multiprocessing
from multiprocessing import Pool
import time
import signal


def worker():
    while True:
        print time.time()
        time.sleep(.5)

def worker_init():
    # ignore the SIGINI in sub process, just print a log
    def sig_int(signal_num, frame):
        print 'signal: %s' % signal_num
    signal.signal(signal.SIGINT, sig_int)


pool = Pool(2, worker_init)
result = pool.apply_async(worker)
while True:
    try:
        result.get(0xfff)
    # catch TimeoutError and get again
    except multiprocessing.TimeoutError as ex:
        print 'timeout'