# My private notebook for practicing python

rabbitmq : An Unacknowledged message implies that it has been read by your consumer, but the consumer has never sent back an ACK to the RabbitMQ broker to say that it has finished processing it.
https://www.cnblogs.com/koka24/p/5304454.html 代码示例比较清楚

2019-08-31
TODO
1. 垃圾回收 https://testerhome.com/topics/16556
http://patshaughnessy.net/2013/10/30/generational-gc-in-python-and-ruby
https://www.jianshu.com/p/1e375fb40506

垃圾收集机制是『引用计数法 Reference Counting

2. mq
https://www.cnblogs.com/koka24/p/5304454.html
3. 内存优化, 当main中启线程时，再fork，会把整个内存数据复制到fork出来的process中，
https://www.cnblogs.com/xybaby/p/7488216.html
https://juejin.im/entry/5d37cc45e51d454f723025d9
4. deepcopy
https://www.cnblogs.com/richardzhu/p/4723750.html
5. collection, argparse,
# https://docs.python.org/zh-cn/3/library/collections.html
6. redis缓存效率
https://www.cnblogs.com/kangoroo/p/7647052.html
7. thread join, daemon,
8. singleton
https://zhuanlan.zhihu.com/p/37534850

#  check, 继承类修改了基类的golbal var, 另一个继承类看到的基类的这个变量是改之前的还是之后的
inheritation/case.py
inheritation/case2.py


2019-08-29 TODO

1. redis, efficience https://realpython.com/python-redis/#more-data-types-in-python-vs-redis
2.

# TODO check, 继承类修改了基类的golbal var, 另一个继承类看到的基类的这个变量是改之前的还是之后的
>>>>>>> origin/master
# https://stackoverflow.com/questions/6501121/difference-between-exit-and-sys-exit-in-python
# exit is a helper for the interactive shell - sys.exit is intended for use in programs.

# https://zhuanlan.zhihu.com/p/37534850
# singleton

# Running a method as a background thread in Python
#  done, exit/exit_daemon.py

# python try catch else,
exception/exceptions.py

# https://docs.python.org/2/library/collections.html#collections.namedtuple
#

# function list
- logging
- classmethon
- itertools
- json
- multiprocess
- import

# abstract class, abc, ABC
https://www.python-course.eu/python3_abstract_classes.php
# reading list
https://jeffknupp.com/blog/2014/06/18/improve-your-python-python-classes-and-object-oriented-programming/

# timeit to measure the execution time

# TODO
super()
inheritance

pytest

优先处理多进程， queue , consumer 并行的问题。

mongo 查询， 筛选列，不全部显示

如何保证进程执行完后状态及时更新到mongo, 而不是一堆doing

如何捕获异常， 有时候内层的异常未track.

# something to be overcomed
- when get error, first thing to do is figure out what the problem really is.
I always fail to do that because lacking of patience to read the error message clearly.
-

# 收集的学习与练习资料
https://pycoders.com/one-more-step
https://realpython.com/run-python-scripts/

# underscore
https://stackoverflow.com/questions/1301346/what-is-the-meaning-of-a-single-and-a-double-underscore-before-an-object-name
Single Underscore

Names, in a class, with a leading underscore are simply to indicate to other programmers that the attribute or method is intended to be private. However, nothing special is done with the name itself.

Double Underscore (Name Mangling)

From the Python docs:

    Any identifier of the form __spam (at least two leading underscores, at most one trailing underscore) is textually replaced with _classname__spam, where classname is the current class name with leading underscore(s) stripped. This mangling is done without regard to the syntactic position of the identifier, so it can be used to define class-private instance and class variables, methods, variables stored in globals, and even variables stored in instances. private to this class on instances of other classes.

And a warning from the same page:

    Name mangling is intended to give classes an easy way to define “private” instance variables and methods, without having to worry about instance variables defined by derived classes, or mucking with instance variables by code outside the class. Note that the mangling rules are designed mostly to avoid accidents; it still is possible for a determined soul to access or modify a variable that is considered private.

__foo__: this is just a convention, a way for the Python system to use names that won't conflict with user names.

_foo: this is just a convention, a way for the programmer to indicate that the variable is private (whatever that means in Python).

__foo: this has real meaning: the interpreter replaces this name with _classname__foo as a way to ensure that the name will not overlap with a similar name in another class.

class level and instance level variables
https://www.digitalocean.com/community/tutorials/understanding-class-and-instance-variables-in-python-3

不可中断的睡眠状态
w    S       进程状态(D=不可中断的睡眠状态,R=运行,S=睡眠,T=跟踪/停止,Z=僵尸进程)
