# coding=utf8
import logging
import os
import logging.config
import yaml
from config.base import root_path


def setup_logging(
        default_path='logging.yaml',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
        # logger = logging.getLogger('dev')
    else:
        logging.basicConfig(level=default_level)
    return logging


#
# logger = setup_logging().getLogger("my_module")
# samplelogger = setup_logging().getLogger("sample")
# logger.debug("debug")
# logger.info("info")
# logger.warning("warn")
#
# samplelogger.info("samplelogger test")


#
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
#
# # create a file handler
# handler = logging.FileHandler("test.log")
# handler.setLevel(logging.DEBUG)
#
# # create a logging format
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)

# # add the handlers to the logger
# logger.addHandler(handler)
#
# logger.info('Hello baby')
# logger.debug('Hello baby debug')
#
#
# logger.info("start log")
# logger.debug("start log debug")


class Logger(object):
    def __init__(self, name, log_level=logging.DEBUG, file_name="default.log"):
        name = name.replace('.log', '')
        logging.basicConfig(level=log_level)
        logger = logging.getLogger(name)
        # logger.setLevel(logginlevel)

        self.handler = logging.FileHandler(file_name)
        self.handler.setLevel(log_level)

        formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s %(message)s')
        self.handler.setFormatter(formatter)

        logger.addHandler(self.handler)
        self._logger = logger

    def get(self):
        return self._logger

    def release(self):
        self.handler.close()
        self._logger.removeHandler(self.handler)


#
with open(os.path.join(root_path, 'config', "logging.yaml"), 'r') as f:
    ycfg = yaml.load(f)
    ycfg.setdefault('version', 1)
    logging.config.dictConfig(ycfg)

logger = logging.getLogger("spider")
#
# alogger = Logger('test', logging.DEBUG).get()
# alogger.debug("t aa ")

# consensus_logger = logging.getLogger("data_prd_consensus")
#
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
#
# logger.info('Start reading database')
# # read database here
# # records = {'john': 55, 'tom': 66}
# # logger.debug('Records: %s', records)
# logger.debug('Updating records ...')
# # update records here
# logger.info('Finish updating records')
# logger.debug("debug test")

# import logging

# https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
