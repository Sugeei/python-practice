# coding=utf8
from multiprocessing import Process
import gc

# for 循环中加进程控制， 其它所有进程都可以并行， 有一个只能一次性执行一个， 因为内存的关系， 测试看是否可以这么操作
catrgorylist = range(5)

import time


def run_event_summary(i):
    print(i)
    time.sleep(5)
    print(i)


def schedule_event_summary():
    # 内存不够，单独跑这一个, 在主进程里跑完内存不释放。。。不能放这里
    # get_event_data_analyst_rating_change()
    gc.collect()

    plist = []
    for event in catrgorylist:
        p = Process(target=run_event_summary, args=(event,))
        # p.start()
        if event == 1:
            for ps in plist:
                ps.join()
            p.start()
            p.join()
        else:
            p.start()
            plist.append(p)

        while len(plist) >= int(3):
            plist = [p for p in plist if p.is_alive()]
            # print("alive processes %s" % len(res_list))
            time.sleep(1)


if __name__ == "__main__":
    schedule_event_summary()
