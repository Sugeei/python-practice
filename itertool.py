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

a = [0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0]

print ("---- itertools.groupby ----")
# print sorted([len(list(group)) for key, group in itertools.groupby(a)])[-1]

# ```
# itertools.groupby方法类似sql语法中的groupby, 用于给数据分组。但不同于sql中按值分组， itertools.groupby按值与位置两个条件分组。值相待且相邻才会归为一组。然后可以对每个组做类似sql中的那种聚合运算。
# 上面例子中用的是求每组长度的运算，这样可以得到各连续子串的长度，再取最大值即可。

###cycle
"""
考虑一个问题。
有一组数据，可以看成是一个矩阵， 共10000行。多少列不重要，假设5列。
想要为这个矩阵添加这样一列数据： 按照
0，1，2，3
的顺序循环取值，即为，
```
0，
1,
2,
3,
0,
1,
2，
3，
0
...
```
当然，还是可以写for循环。
只是

还是只需要一行而已。不过复杂一点的是，添加这样一列数据需要用到生成器。

```
"""

iter = itertools.cycle('0123')
print ("---- itertools.cycle ----")
# print iter.next()
# print iter.next()
# print iter.next()
# print iter.next()
# print iter.next()

def get_iter_index(df, w):
    # 参数 df 是一个pandas dataframe, 可以理解为是一个矩阵，由行列数据构成
    # 参数 w 用于指定生成的待循环数据。当然也可以直接传入一个
    # # 造数据列， index
    iters = itertools.cycle(range(w))
    df['iter_index'] = 0
    for i in range(df.shape[0]):
        df.iloc[i, 31] = iters.next()
    return df


# generator, next,
# yield

# http: // www.liaoxuefeng.com / wiki / 00143160
# 89557264
# a6b348958f449949df42a6d3a2e542c000 / 00143200162233153
# 835
# cfdd1a541a18ddc15059e3ddeec000


# How to sort a Python dict by value
# (== get a representation sorted by value)

xs = {'a': 4, 'b': 3, 'c': 2, 'd': 1}

xx = sorted(xs.items(), key=lambda x: x[1])
# [('d', 1), ('c', 2), ('b', 3), ('a', 4)]
# sorted(xs.items(), key=lambda x:x[])
print(xs)
print(sorted(xs.items(), key=lambda x: x[0]))
# Or:
print(xx)

# >>> import operator
# >>> sorted(xs.items(), key=operator.itemgetter(1))
# [('d', 1), ('c', 2), ('b', 3), ('a', 4)]
