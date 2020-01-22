from feed.sse import FeedSSE
from feed.szse import FeedSZSE
from dao.access import accessbase
from config.logger import logger
import pandas as pd


# TODO get listed company info
# to filter target info

class CategoryListedCompany():
    def __init__(self):
        self.sseobj = FeedSSE()
        self.zseobj = FeedSZSE()
        self.output_sse = pd.DataFrame()
        self.output_zse = pd.DataFrame()

    def output(self):
        self.sseobj.transform(self.output_sse, self.sseobj.__class__.__name__)
        self.zseobj.transform(self.output_zse, self.zseobj.__class__.__name__)

    def get(self, id, flag):
        flag = flag.strip()
        if flag == '上海':
            # return FeedSSE()
            r = self.access(self.sseobj, id)
            self.output_sse = pd.concat([self.output_sse, r])
            # self.sseobj.transform(self.output_sse, self.sseobj.__class__.__name__+str(id))
        elif flag == '深圳':
            r = self.access(self.zseobj, id)
            self.output_zse = pd.concat([self.output_zse, r])
            # self.zseobj.transform(self.output_zse, self.zseobj.__class__.__name__+str(id))

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
