import os
import sys


def linux_interaction():
    assert ('linux' in sys.platform), "Function can only run on Linux systems."
    print('Doing something.')


# os.fork()is only available in Unix.
try:
    linux_interaction()
except:
    print('Linux function was not executed')
    pass


def child():
    print('\nA new child ', os.getpid())
    os._exit(0)


def parent():
    while True:
        newpid = os.fork()
        if newpid == 0:
            child()
        else:
            pids = (os.getpid(), newpid)
            print("parent: %d, child: %d\n" % pids)
        reply = input("q for quit / c for new fork")
        if reply == 'c':
            continue
        else:
            break


parent()
