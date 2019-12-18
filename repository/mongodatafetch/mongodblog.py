# 统计mongodb中 posinfo 数据量并写入log文件


import time, re, datetime
import pymongo
import csv
from xlswriter import excelwriter
from mongoconn import mongoset, mongoinsert,mongoupdate, TPOS


table_comp = TPOS