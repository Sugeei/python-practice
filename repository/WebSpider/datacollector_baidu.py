# -*- coding: utf-8 -*-
#
import time
import pymongo
from datetime import datetime
from mongoconn import mongoset


dbconn = mongoset('datacourse', 'advertiserinfo')

time = datetime.now()
filename = 'baidu_ad_list_' + time.strftime('%Y-%m-%d') + '.csv'

def transcode(s):
    return str(s).encode('utf-8').decode('utf-8')

def get_all_data():
    title = []
    with open('data.csv', encoding="utf-8", mode='w+') as f:
        for i in dbconn.find().sort("timestamp", pymongo.DESCENDING):#sort( { "timestamp": 1 } ):
            if not title:
                title = list(i.keys())
                title.sort()
                f.writelines(','.join(title) + '\n')

            key = list(i.keys())
            key.sort()

            value = [i[k] for k in key]
            value = map(transcode, value)

            a = ','.join(value).encode('utf-8').decode('utf-8')
            f.writelines(a + '\n')
    #print(dbconn.find())

if __name__ == "__main__":

    get_all_data()