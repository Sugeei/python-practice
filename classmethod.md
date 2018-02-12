```
def f(x,l=[]):

for i in range(x):

l.append(i*i)

print (l)

f(2)

f(3,[3,2,1])

f(3)

```

```

>>>

[0, 1]

[3, 2, 1, 0, 1, 4]

[0, 1, 0, 1, 4] # 使用了第一次调用时存储的旧列表。python2.7. why

>>>

```



>做到了支持封闭性与扩展性

工厂模式

http://pythoncentral.io/difference-between-staticmethod-and-classmethod-in-python/

Meaning of @classmethod and @staticmethod for beginner?https://stackoverflow.com/questions/12179271/meaning-of-classmethod-and-staticmethod-for-beginner



iterator, python 实现二叉树中序遍历

```

#!usr/bin/env python

#_*_ coding: utf-8 _*_

#  python 2.7

#  get info from xiaozhuduanzu

from bs4 import BeautifulSoup

import requests

import os

import urllib

import itertools

# define iterator

def reversedIterator(object):

def __init__(self, list):

self.list = list

self.index = len(list)

def __iter__(self):

return self

def next(self):

self.index -= 1

if self.index >=0:

return self.list[self.index]

else:

raise StopIteration

class BinaryTree(object):

def __init__(self, value, left=None, right=None):

self.value = value

self.left=left

self.right = right

def __iter__(self):

return PreorderIterator(self)

class PreorderIterator(object):

def __init__(self, node):

self.node = node

self.stack = []

self.stack.append(self.node)

def next(self):

# if len(self.stack) == 0 and self.node is not None: self.stack.append(self.node)

if len(self.stack) > 0 :#and self.node is not None:

# self.node = self.node.left

self.node = self.stack.pop()

# self.node = self.node.left

if self.node.right is not None: self.stack.append(self.node.right)

if self.node.left is not None: self.stack.append(self.node.left)

return self.node.value

else:

raise StopIteration()

class InorderIterator(object):

def __init__(self, node):

self.node = node

self.stack = []

def next(self):

if len(self.stack) > 0 or self.node is not None:

while self.node is not None:

self.stack.append(self.node)

self.node = self.node.left

node = self.stack.pop()

self.node = node.right

return node.value

else:

raise StopIteration()

if __name__ == "__main__":

tree = BinaryTree(

left = BinaryTree(

left = BinaryTree(1),

value = 2,

right = BinaryTree(

left = BinaryTree(3),

value=4,

right=BinaryTree(5)

),

),

value = 6,

right = BinaryTree(

value = 7,

right=BinaryTree(8)

)

)

for value in tree:

print(value)

# x = {'a': 1, 'b': 2, 'c': 3}

# i = x.iteritems()

# print(x.iteritems())

# x=[2,4,5]

# a= reversed(x)

# print(a.next())

# print(a.next())

# print(a.next())

# # print(a.next())

# print(reversed(x))

#

# for i in reversed(x):

#    print(i)

# # print(reversed(x))

# for i, n in enumerate(x):

#    print(i,n)

```