# coding=utf8
import multiprocessing as ms
import time
import os


class MyProcess(ms.Process):
    def run(self):
        print("process", os.getpid())

    def __del__(self):
        print("deleted")


def main():
    p1 = MyProcess()
    p2 = MyProcess()
    p1.start()
    time.sleep(1)
    p2.start()
    time.sleep(1)
    p2.join()  # 等待进程结束
    # print(ms.active_children())
    # while True:
    #     time.sleep(0.01)


if __name__ == "__main__":
    main()
    while True:
        time.sleep(10)