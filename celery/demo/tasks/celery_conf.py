from celery import Celery
import os
import logging.config


def load_log_config():
    base_dir = os.path.abspath(".")
    log_dir = base_dir + "/logs"
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    logging.config.fileConfig(base_dir + "/log.conf", defaults={'log_dir': log_dir})


def getLogger(logger_name):
    load_log_config()
    return logging.getLogger(logger_name)

log = getLogger("worker")
app = Celery('tasks',
             broker='amqp://guest:guest@localhost:5672//')

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

