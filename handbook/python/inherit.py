# coding=utf8
# python 2.7
import os

# 子类共用父类的部分变量
class Parent(object):
    DEFAULT_VALUE = 'parent'
    var = 0
    p = 1
    # def __init__(self):
    #     self.var = 0
    #     self.parenta = 1

    def func1(self):
        print 'parent : ' + self.DEFAULT_VALUE


class Child(Parent):
    DEFAULT_VALUE = 'child'

    # 继承类定义的同名函数会覆盖父类的定义。 init中初始化的变量也是一样。
    def __init__(self):
        # self.DEFAULT_VALUE = 'a'
        # self.var = super.var
        self.p = 3

    def update_value(self):
        print 'before : ' + self.DEFAULT_VALUE
        self.DEFAULT_VALUE = 'updated_child_value'
        print 'after : ' + self.DEFAULT_VALUE

    def update_value_reset(self):
        print 'reset before  : ' + self.DEFAULT_VALUE
        self.DEFAULT_VALUE = 'child'
        print 'reset after : ' + self.DEFAULT_VALUE


if __name__ == '__main__':
    c = Child()
    c.update_value()
    c.func1()
    print 'child value : ' + c.DEFAULT_VALUE
    d = Child()  # 新对象
    d.func1()
    # Output：
    # before: child
    # after: updated_child_value
    # parent: updated_child_value
    # child
    # value: updated_child_value
    # parent: child
    # if __name__ == '__main__':
    #     c = Child()
    #     c.update_value()
    #     c.func1()
    #     c.update_value_reset()
    #     c.func1()
    # Output：
    # before: child
    # after: updated_child_value
    # parent: updated_child_value
    # reset
    # before: updated_child_value
    # reset
    # after: child
    # parent: child
