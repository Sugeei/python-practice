import pandas as pd
import os
# from config.base import listedcompanies
from config.logger import logger
from interface.base import Base
from category.landinfo import CategoryLandInfo
from dao.access import accessbase


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

    # if __name__ == '__main__':
    # InterFaceLandInfo().run()


if __name__ == "__main__":
    url = "https://www.landchina.com/default.aspx?tabid=386&comname=default&wmguid=75c72564-ffd9-426a-954b-8ac2df0903b7&recorderguid=9A59E61025A951EDE055000000000001"
    url = "https://www.landchina.com/default.aspx?tabid=386&comname=default&wmguid=75c72564-ffd9-426a-954b-8ac2df0903b7&recorderguid=d226523a-88df-4c1e-b183-a004b8a560b1"
    us = [url]
    CategoryLandInfo().get_detail(us)
    # title, page = accessbase.get_with_proxy(url)
