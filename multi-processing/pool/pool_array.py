import multiprocessing
import ctypes
import numpy as np

shared_array_base = multiprocessing.Array(ctypes.c_double, 10 * 10)
shared_array = np.ctypeslib.as_array(shared_array_base.get_obj())
shared_array = shared_array.reshape(10, 10)


# -- edited 2015-05-01: the assert check below checks the wrong thing
#   with recent versions of Numpy/multiprocessing. That no copy is made
#   is indicated by the fact that the program prints the output shown below.
## No copy was made
##assert shared_array.base.base is shared_array_base.get_obj()

# Parallel processing
def my_func(i, def_param=shared_array):
    shared_array[i, :] = i


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=4)
    pool.map(my_func, range(10))

    print shared_array
