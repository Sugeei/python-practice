#!/usr/bin/python
# -*- coding: UTF-8 -*

#  multiprocess
#  TODO: format data to insert into database for recruitment db

from multiprocessing import Pool
import time, re
import pymongo

class formatdata:
    def __init__(self, keys):
        # keys is a list
        self.keys = keys

    def getformatdata(self, source):
        data = {}
        for item in self.keys:
            data[item] = ''
            if source[item]:
                data[item] = source[item]
        return data

    def getformatdict(self, key, value):
        if type(key) is not list:
            key = list(key)

        if type(value) is not list:
            value = list(value)

        data = self.keys
        for k,v in zip(key, value):
            try:
                data[k] = v
            except:
                pass
        return data

    def get_format_dict(self, value):
        # if type(key) is not list:
        #     key = list(key)
        key = self.keys
        if type(value) is not list:
            value = list(value)

        data = {}
        for k, v in zip(key, value):
            try:
                data[k] = v
            except:
                pass
        return data


Fdata = formatdata({
    '_id': '',
    'itemurl': '',
    'flag': False,
})

if __name__ == '__main__':

    keys = ['itemurl', 'flag']
    format = formatdata(keys)

    source = {
        'itemurl':'kkk',
        'flag':False,
    }

    print(format.getformatdata(source))

    source = ['a','b']
    print(format.getformatdict(source))