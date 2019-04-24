# coding=utf8

# to read a.txt under folder data
# /import
#   /data
#      /a.txt
#   /submodule
#     /subscript.py

import os

print os.path.dirname(os.path.realpath(__file__))

# return the abspath of the current script
dir = os.path.dirname(os.path.realpath(__file__))


# when run subscript.py,  ***\import\submodule

with open(os.path.join(os.path.dirname(dir), "data", "a.txt"), 'r') as f:
    c = f.read()
    print c
