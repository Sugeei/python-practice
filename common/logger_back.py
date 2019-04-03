# coding=utf8
import logging
import os
import sys
import logging.config
import yaml

# the folder of current py file
this_dir = os.path.dirname(os.path.realpath(__file__))
# the parent folder
base_dir = os.path.dirname(this_dir)


def setup_logging(
        default_path=os.path.join(this_dir, 'logging.yaml'),
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
        # logging.config.fileConfig(config)
        # logger = logging.getLogger('dev')
    else:
        logging.basicConfig(level=default_level)
    return logging


if not os.path.exists(base_dir + "/logs"):
    os.mkdir(base_dir + "/logs")

try:
    # this will get the path from where to run
    main_module = sys.modules['__main__'].__file__
    module_dir = os.path.dirname(main_module)
    logger_name = module_dir[module_dir.rfind('/') + 1:]
    print "main module is %s, logger name is %s" % (main_module, logger_name)
except Exception, err:
    logger_name = ""

logger = setup_logging().getLogger(logger_name)


# logger.addHandler()

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


import logging
import sys
from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = os.path.join(base_dir, "logs", "%s.log" % logger_name)


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger

# https://www.toptal.com/python/in-depth-python-logging
