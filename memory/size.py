# There is a module called Pympler which contains the asizeof module.
#
# Use as follows:
#
# from pympler import asizeof
# asizeof.asizeof(my_object)
#
# Unlike sys.getsizeof, it works for your self-created objects.
#
# >>> asizeof.asizeof(tuple('bcd'))
# 200