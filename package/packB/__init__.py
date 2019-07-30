## this import makes a1_func directly accessible from packA.a1_func
# from package.packagepackA.a1 import a1_func
#

from .a1 import a1_func
def packA_func():
    print("running packA_func()")
