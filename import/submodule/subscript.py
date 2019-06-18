# coding=utf8

# to read a.txt under folder data
# /import
#   /data
#      /a.txt
#   /submodule
#     /subscript.py

# forward slash vs backslash
# https://lerner.co.il/2018/07/24/avoiding-windows-backslash-problems-with-pythons-raw-strings/
import os
print os.path.normpath("c:/aDirname/")
print r'abc\tab'
print 2
print __file__
print os.path.realpath(__file__)
print 5
print __name__
print os.path.dirname(os.path.realpath(__file__))
print 110
print os.path.dirname(__file__)

# return the abspath of the current script
dir = os.path.dirname(os.path.realpath(__file__))


# when run subscript.py,  ***\import\submodule

with open(os.path.join(os.path.dirname(dir), "data", "a.txt"), 'r') as f:
    c = f.read()
    print c
