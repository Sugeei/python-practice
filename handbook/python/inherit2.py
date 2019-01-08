# coding=utf8
# python 2.7
import os


class P(object):
    def __init__(self):
        self.value = 0
        self.a = 0

    def get(self):
        print self.value
        return id(self.value)


class C(P):
    def __init__(self):
        super(C, self).__init__()  # 标准的写法是这样的, 先调用父类构造函数
        self.value = 44  # 两句交换一下位置看看

a = C()
print C().get()
