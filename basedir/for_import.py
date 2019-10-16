# from basedir import config
from basedir.config.config import base_dir
import os

this_dir = os.path.dirname(os.path.realpath(__file__))
print('for import')
print(this_dir)
# run config.py, this_dir will be root.../common

# __file__ represents the real path of current python file, even when the current file is been imported from other folder