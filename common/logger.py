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


try:
    # this will get the path from where to run
    main_module = sys.modules['__main__'].__file__
    module_dir = os.path.dirname(main_module)
    #
    # create folder for log
    if not os.path.exists(module_dir + "/logs"):
        os.mkdir(module_dir + "/logs")
    logger_name = module_dir[module_dir.rfind('/') + 1:]
    print "main module is %s, logger name is %s" % (main_module, logger_name)
except Exception, err:
    logger_name = ""

logger = setup_logging().getLogger(logger_name)
