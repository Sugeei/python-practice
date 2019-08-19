# coding=utf8
import os, argparse
from collections import ChainMap

# 让用户指定的命令行参数优先于环境变量，优先于默认值的例子
defaults = {'color': 'red', 'user': 'guest'}

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user')
parser.add_argument('-c', '--color')
namespace = parser.parse_args()
command_line_args = {k: v for k, v in vars(namespace).items() if v}

combined = ChainMap(command_line_args, os.environ, defaults)
print(combined['color'])
print(combined['user'])

# below shows how to call it in git bash
# D:/python/conda/envs/consensus/python chain_map.py -u damin -c blue

#
# import builtins
# pylookup = ChainMap(locals(), globals(), vars(builtins))
