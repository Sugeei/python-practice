# coding=utf-8

import logger
logger.basicConfig(level=logger.INFO)
print (__name__)
logger = logger.getLogger(__name__)

logger.info('Start reading database')
# read database here
records = {'john': 55, 'tom': 66}
logger.debug('Records: %s', records)
logger.info('Updating records ...')
# update records here
logger.info('Finish updating records')

from common.logger import data_log

data_log.info("first message form logger")