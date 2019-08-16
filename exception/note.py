# ImportError: cannot import name namedtuple
遇到两次在使用multiprocessing时出来这种报错都是因为自己的某个python文件与引用包里的名字重了。
避免使用过于简单的文件名像：collection, cache, operator
