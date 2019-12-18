# !/usr/bin/python
# -*- coding: utf-8 -*-

import re
import scrapy
import os
import datetime, time

pronoun = 'I, you, your, he, she, it, we, you, they, me, him, her, it, us, them'
pronoun = 'I, you'
pronoun = pronoun.split(',')
pronouns = [item.strip() for item in pronoun]

# !/usr/bin/python
# -*- coding: utf-8 -*-

class counter(object):
    count = 5
    def __init__(self):
        # __calss__ 用于访问类的公共变量, 此处访问的是变量 count
        self.__class__.count += 1
        # self.count = 0
        self.getcount()

    def getcount(self):
        print(self.count)


if __name__ == '__main__':
    print(counter.count) # 初始值为5
    a = counter() # count 自加1得6, 由于是公共变量, 所有counter类的实例共享同个一count变量, 对python来说是引用同一个对象
    print(counter.count)  # 也为6
    b = counter() # count 再自加1得7
    print(counter.count)  # 也为7
    b.count += 3
    b.getcount()
    a.getcount()
    c = counter()
    print(counter.count)  # 也为7
    a.getcount()
    b.getcount()