# coding=utf-8

import logging
logging.basicConfig(level=logging.INFO)
# print (__name__)
data_log = logging.getLogger("data_log")
flow_log = logging.getLogger("flow_log")


# create a file handler
handler = logging.FileHandler('logs/data.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
data_log.addHandler(handler)

handler = logging.FileHandler('logs/flow.log')
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
flow_log.addHandler(handler)
