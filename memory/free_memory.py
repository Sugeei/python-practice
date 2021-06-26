# https://stackoverflow.com/questions/39100971/how-do-i-release-memory-used-by-a-pandas-dataframe

import os, psutil, numpy as np


def usage():
    process = psutil.Process(os.getpid())
    return process.memory_full_info()[0] / float(2 ** 20)


print(usage())  # initial memory usage
# 27.5


arr = np.arange(10 ** 8)  # create a large array without boxing
usage()
print("3")  #
print(usage())  #

# 790.46875
del arr
usage()
print("4")  #

print(usage())  #

# 27.52734375 # numpy just free()'d the array

arr = np.arange(10 ** 8, dtype='O')  # create lots of objects
print("5")  #
print(usage())  #

# 3135.109375
del arr
# usage()
print("6")  #
import time
# time.sleep(3) # wait won't work
print(usage())  #
#

# import pandas as pd
#
# df = pd.read_csv("dmkt_equd_all_technical_columns20190703.csv")
# print(usage())  #
# print(df.info(memory_usage='deep'))
# del df
# print(usage())  #
#
# import gc
# gc.collect()
# print("finally")
# print(usage())  #
