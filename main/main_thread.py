from threading import Thread
import time

var = 1

class ThreadDemo(Thread):
    def __init__(self):
        # by default, daemon is false,
        pass

    def run(self):
        while True:
            print("thread run %s " % var)
            time.sleep(1)


# https://docs.python.org/3/library/threading.html
# In normal conditions, the main thread is the thread from which the Python interpreter was started

#
# daemon
#
#     A boolean value indicating whether this thread is a daemon thread (True) or not (False). This must be set before start() is called, otherwise RuntimeError is raised. Its initial value is inherited from the creating thread; the main thread is not a daemon thread and therefore all threads created in the main thread default to daemon = False.
#
#     The entire Python program exits when no alive non-daemon threads are left.

if __name__ == "__main__":
    print("main start")
    ThreadDemo().run()
    print("main exit")

# 测试结果