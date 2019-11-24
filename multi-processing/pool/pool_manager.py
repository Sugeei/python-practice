# TODO How to share a very big dictionary among processes in Python

#  pool manager seems to solve the problem about sharing a very large dict(about 160M) between processes.
from multiprocessing import Manager

manager = Manager()
# init_data = manager.dict(dict)
# pool.apply_async(func, args=(init_data))

# TODO broken pipe errro
# on docker , raise error
# https://stackoverflow.com/questions/3649458/broken-pipe-when-using-python-multiprocessing-managers-basemanager-syncmanager
# http://382306.com/News/index.php?i=1887&u=//questions/51301392/python-multiprocessing-queue-broken-pipe-connection-reset-by-peer

# https://stackoverflow.com/questions/48950516/python-multiprocessing-pool-apply-async-error

# TODO
# https://docs.python.org/3.5/library/multiprocessing.html?highlight=multiprocessing#multiprocessing-programming
# TODO why
# Better to inherit than pickle/unpickle

