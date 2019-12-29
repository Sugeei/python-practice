import pandas as pd
import os
from config.base import listedcompanies
from config.logger import logger
from interface.base import Base
from category.landinfo import CategoryLandInfo


class InterFaceLandInfo(Base):
    """
    interface connect task and response.
    as there may have more than one way to get target info, should manage all the feed obj, to collect their output

    """

    def __init__(self):
        # self.src_info = listedcompanies
        self.obj = CategoryLandInfo()
        logger.info("%s init" % self.__class__.__name__)

    def run(self):
        self.obj.get()
        self.obj.output()
        # res = pd.DataFrame([], columns=['key', 'value'])
        # for item in self.src_info:
        #     tid, city = self.format(item)
        #     self.obj.get(tid, city)
        # self.obj.output()
        # # res = pd.concat([res, r])
        # self.selftransform(res, self.__class__.__name__)
        # res.to_csv('%s.csv' % self.__class__.__name__, index=False)


if __name__ == '__main__':
    InterFaceLandInfo().run()
