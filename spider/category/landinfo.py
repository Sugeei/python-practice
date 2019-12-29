from feed.landchina import FeedLand
from dao.access import accessbase
from config.logger import logger
import pandas as pd

import time
# TODO get listed company info
# to filter target info

class CategoryLandInfo():
    def __init__(self):
        self.feed = FeedLand()
        self.result_set = pd.DataFrame()

    def output(self):
        self.feed.transform(self.result_set, self.feed.__class__.__name__)

    def get(self):
        title, page = accessbase.get(self.feed.get_src_url())
        s = self.feed.get_soup(page)
        suburls =  self.feed.get_sub_urls(s)
        for id, u in enumerate(suburls):
            title, page = accessbase.get(u)
            logger.info("%s url=%s, get title=%s, content length=%s" % (self.__class__.__name__, u, title, len(page)))
            if '403' in title:
                time.sleep(10)
            s = self.feed.get_soup(page)
            res = self.feed.get_target_info(s)
            logger.info("%s url=%s, get res_length=%s" % (self.__class__.__name__, u, len(res)))
            df = pd.DataFrame(res, columns=['key', 'value'])
            df['id'] = id
            self.result_set=pd.concat([self.result_set, df])

    def access(self, feedobj, id):
        try:
            url = feedobj.get_src_url(id)
            logger.info("%s url=%s" % (self.__class__.__name__, url))
            title, page = accessbase.get(url)
            logger.info("%s url=%s, get title=%s, content length=%s" % (self.__class__.__name__, url, title, len(page)))
            s = feedobj.get_soup(page)
            res = feedobj.get_cn_con(s)
            logger.info("%s url=%s, get res length=%s" % (self.__class__.__name__, url, len(res)))
        except:
            res = []
        a = pd.DataFrame(res, columns=['key', 'value'])
        a['id'] = id
        return a
        # return
