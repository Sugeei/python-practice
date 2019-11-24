# from common import config

filename = 'robt.txt'
print(filename.rpartition('.'))

four_lists = [[] for __ in range(4)]
print(four_lists)

string = "Deepak is a good person and Preeti is not a good person."
print(string.partition('is '))
# 'is' separator is found at every occurence print(string.partition('is '))
print(string.split('is '))
print(string.rpartition('is '))
print(string.partition('is'))

d = {'hello': 'world'}
if 'hello' in d:
    print(d['hello'])
else:
    print('bye')

import flask

import requests
r = requests.get('http://baidu.com')
r.status_code