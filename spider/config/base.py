import os
import re
import pandas as pd

phantomjs = '/usr/local/bin/phantomjs-2.1.1-macosx/bin/phantomjs'
# binphantomjs = '/Users/shujinhuang/Documents/pythonworks/python-practice/spider/phantomjs-2.1.1-macosx/bin'

root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

with open(os.path.join(root_path, 'data', 'listedcompany_ids'), 'r') as f:
    listedcompanies = f.readlines()
listedcompanies = [x.replace("(","").replace(")","").strip().split('/') for x in listedcompanies]
# listedcompanies = [x.strip().split('/') for x in listedcompanies]


# listedcompanies = [re.findall('\d{6}', x.strip())[0] for x in listedcompanies]
pass
# re.findall('\d{4}', '0000abc')
