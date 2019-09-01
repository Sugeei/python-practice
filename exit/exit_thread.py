# coding:utf8
import time
from threading import Thread
import sys
from datetime import datetime, timedelta

status = True


class SyncStatus(Thread):
    """
        """

    def __init__(self):
        Thread.__init__(self)
        Thread.setName(self, "SyncStatus")
        self.setDaemon(True)
        self.interval = 30
        self.timestamp = datetime.now()

    def run(self):
        i = 0
        while True:
            try:
                i += 1
                print(i)
                time.sleep(1)
                if i == 3:
                    raise ValueError
            except Exception as err:
                # status = False
                print("sync exception %s" % err)
                # sys.exit(1) # can exit main.py
                exit(2) # can exit main.py


if __name__ == "__main__":
    SyncStatus().start()
    while True:
        time.sleep(100)

    print('exit') # will not be executed
