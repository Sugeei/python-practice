import pymongo

from filereader import xlsxreader
from mongoconn import mongoset, mongoinsert,mongoupdate
from formatdata import formatdata

filename = 'companylist.xlsx'

data = xlsxreader(filename)

# comp = mongoset('lieping', 'complist')
#
comp = mongoset('openpositiondb', 'complist')
# comp.create_index([('officialsite', pymongo.DESCENDING)], unique=True)

# title = ['idx', 'sponser','company','industry','company', 'level', 'startfrom', 'officialsite', '', '']
title = ['idx', 'sponser','company', 'financial_level', 'finance_status', 'startfrom', 'officialsite', 'product', 'comment']
format = formatdata(title)
# flag = 0
# print(data.rows)
complist = []
for row in data.rows:
    # if flag == 0:

    item = []
    for cell in row:
        item.append(cell.value)
        print(cell.value)
    # flag = 1
    complist.append(item)


complist = complist[1:]

for item in complist:

    try:
        comp.insert_one(format.get_format_dict(item))
        # comp.insert_one(format.getformatdict(item))
    except:
        pass
# print (data)



