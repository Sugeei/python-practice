# -*- coding: utf-8 -*-
# 用于实训营考勤统计
# 格式化输出
# ```
# !/usr/bin/python

# Itertools的打开方式
# keyword: Itertools, groupby

###groupby
# 给定一组数，只含有0跟1，找出其中最长的连续子串（全0串或者全1串）的长度。
# 比如这组数为[0,1,0,0,0,1,1,1,1,0,0,1,1,1,1,1,1,0,0,0]， 其中有连续3个0的子串，有连续4个1的子串，也有连续6个1的子串。比较后发现最长的子串为连续6个1。这就是我们要找出的最长子串，其长度为6。

# 当然可以用for循环扫描整个数组，扫描过程中加上变量，标记用来做统计之类的方法。

# 但是，itertools可以一行代码搞定：
# ```
import itertools

# a = [0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0]
#
# for i in range(10):
#     print i
# else:
#     print i+1

for i in range(10):
    for j in ["a", "b", "c"]:
        if j=='b':
            print j, i
            break # break 内层循环