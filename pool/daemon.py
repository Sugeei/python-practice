import threading
import os
import time


# daemon=True means that this thread has to be closed when the main process done. even the thread has not
# finished yet.
# normally, when the main process done, a thread will not exit with default "daemon=False"
#
def func():
    time.sleep(3)
    print("finish")


def func2():
    time.sleep(2)
    print("finish 2")


# threading.Thread(target=func).start()
threading.Thread(target=func2, daemon=True).start()

# ref
# https://laike9m.com/blog/daemon-is-not-daemon-but-what-is-it,97/