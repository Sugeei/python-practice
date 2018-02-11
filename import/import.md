6.1.2. The Module Search Path
When a module named spam is imported, the interpreter first searches for a built-in module with that name. If not found, it then searches for a file named spam.py in a list of directories given by the variable sys.path. sys.path is initialized from these locations:
the directory containing the input script (or the current directory).
PYTHONPATH (a list of directory names, with the same syntax as the shell variable PATH).
the installation-dependent default.
After initialization, Python programs can modify sys.path. The directory containing the script being run is placed at the beginning of the search path, ahead of the standard library path. This means that scripts in that directory will be loaded instead of modules of the same name in the library directory. This is an error unless the replacement is intended. See section Standard Modules for more information.

当导入名为 spam 的模块时, 解释器会先在当前目录下查找名为 spam.py 的文件, 然后搜索环境变量 PYTHONPATH 记录的所有目录. 这个变量与 shell 变量 PATH 有相同的语法, 它是一些目录名的列表. 当没有设置 PYTHONPATH , 或者在前述各种路径中都没找到期望的文件时, 那么解释器会在pyhton 安裝时定义的默认目录中搜寻. 在 Unix 中, 通常是在/usr/local/lib/python .
实际上, 都是在变量 sys.path 定义的目录列表中搜索模块的, 该变量初始化包含了执行脚本的目录 (或者当前目录) 以及 PYTHONPATH 和与安装时相关的默认目录. 这使得 Python 程序猿在必要的时候,可以直接进行更改或替代相关路径来进行模块搜索.
注意, 因为搜索目录包含当前运行脚本的目录, 所以令脚本名不与某个标准模块重名很重要, 否则 Python 会尝试把这个脚本当成一个模块载入, 而重名系统模块已经被导入时. 这通常会抛出一个错误. 参看 标准模块 小节获取更多信息.

PS:还有一种方式避免上述的问题，就是在每个py文件上的首行引入以下一行
from __future__ import absolute_import
也是可以解决上述问题。

下面将具体介绍几种常用情况：
（1）主程序与模块程序在同一目录下：
如下面程序结构:
`-- src
    |-- mod1.py
    `-- test1.py
若在程序test1.py中导入模块mod1, 则直接使用 import  mod1或from mod1 import *;
（2）主程序所在目录是模块所在目录的父(或祖辈)目录
如下面程序结构:
`-- src
    |-- mod1.py
    |-- mod2
    |   `-- mod2.py
    `-- test1.py
若在程序test1.py中导入模块mod2, 需要在mod2文件夹中建立空文件__init__.py文件(也可以在该文件中自定义输出模块接口); 然后使用 from mod2.mod2 import * 或import mod2.mod2.
（3）主程序导入上层目录中模块或其他目录(平级)下的模块
如下面程序结构:
`-- src
    |-- mod1.py
    |-- mod2
    |   `-- mod2.py
    |-- sub
    |   `-- test2.py
    `-- test1.py
若在程序test2.py中导入模块mod1和mod2。首先需要在mod2下建立__init__.py文件(同(2))，src下不必建立该文件。然后调用方式如下：
下面程序执行方式均在程序文件所在目录下执行，如test2.py是在cd sub;之后执行python test2.py
而test1.py是在cd src;之后执行python test1.py; 不保证在src目录下执行python sub/test2.py成功。
   import sys
   sys.path.append("..")
   import mod1
   import mod2.mod2
 （4）从(3)可以看出，导入模块关键是能够根据sys.path环境变量的值，找到具体模块的路径。
这里仅介绍上面三种简单情况。
以上这篇浅谈python import引入不同路径下的模块就是小编分享给大家的全部内容了，希望能给大家一个参考，也希望大家多多支持脚本之家。

http://blog.konghy.cn/2017/04/24/python-entry-program/