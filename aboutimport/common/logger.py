# coding=utf8
import logging
from logging import config
import os
import yaml
import sys

this_dir = os.path.dirname(os.path.realpath(__file__))
base_dir = os.path.dirname(this_dir)

#
# with open(os.environ['DATA_PROD_HOME'] + "/report/logging.yaml") as f:
#     ycfg = yaml.load(f)
#     ycfg.setdefault('version', 1)
#     logging.config.dictConfig(ycfg)

# logger = logging.getLogger(os.environ['PROD_MODULE'])

with open(this_dir + "/logging.yaml") as f:
    ycfg = yaml.safe_load(f.read())
    ycfg.setdefault('version', 1)
    config.dictConfig(ycfg)

try:
    main_module = sys.modules['__main__'].__file__
    module_dir = os.path.dirname(main_module)

    if not os.path.exists(module_dir + "/logs"):
        os.mkdir(module_dir + "/logs")
    logger_name = module_dir[module_dir.rfind('/') + 1:]
    # print "main module is %s, logger name is %s" % (main_module, logger_name)
except Exception as err:
    logger_name = ""

logger = logging.getLogger(logger_name)

# logger.info("%s launch" % logger_name)
