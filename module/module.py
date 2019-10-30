# !/usr/bin/python
# -*- coding: utf-8 -*-

class modulea():
    def __init__(self):
        __self__ = ''

    def printa(self):
        print( "i am module a")


def printb():
    print( "i am module b")

# https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html

#
# When a module named spam is imported, the interpreter first searches for a built-in module with that name. If not found, it then searches for a file named spam.py in a list of directories given by the variable sys.path. sys.path is initialized from these locations:
#
#     The directory containing the input script (or the current directory when no file is specified).
#     PYTHONPATH (a list of directory names, with the same syntax as the shell variable PATH).
#     The installation-dependent default.
#
# After initialization, Python programs can modify sys.path. The directory containing the script being run is placed at the beginning of the search path, ahead of the standard library path. This means that scripts in that directory will be loaded instead of modules of the same name in the library directory. Source: Python 2 and 3

# TODO 关于module, import, 路径相关， 一直没有整理的特别清楚
#
