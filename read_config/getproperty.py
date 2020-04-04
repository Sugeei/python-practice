# coding=utf8
import configparser
import os

uranus_path = os.path.dirname(os.path.realpath(__file__))
# uranus_path = os.path.dirname('consensuus_config.json')
fname = "const.properties"
fname='config.txt'
uranus_path = os.path.join(uranus_path, fname)
#
with open(uranus_path,'r') as f:
    print(f.read())
config = configparser.ConfigParser()

# 不能给config.read传open()对象
config_file = open(uranus_path, encoding="utf8")
# config.read("const.properties")
config.read(uranus_path, encoding='utf8')
print(config.sections())
d = config['DEFAULT']
print(d)
# config.options("DEFAULT")
option_list = config.items('DEFAULT')

option_dict = {item[0].strip(): item[1].strip() for item in option_list}

print(option_dict)
# print (config['DEFAULT'])

# # 疑难杂症
# 1. configureParser 报错：找不到指定的section如"prd".
# ```
# 检查config.properties文件的编码方式。最好在notepad++将其保存为utf-8编码。如果是ASCII编码文本头会存储"\ufeff"标识，导致configParser识别失败
# ```