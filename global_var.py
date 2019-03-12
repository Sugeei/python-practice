# coding=utf-8

# 不推荐使用全局变量


def foo(x):
    print 'x = ', x
    x = 200
    print 'Changed in foo(), x = ', x


x = 100
foo(x)
print 'x = ', x


