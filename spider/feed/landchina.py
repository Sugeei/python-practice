from feed.abstract import FeedBase


class FeedLand(FeedBase):
    def __init__(self):
        self.url = "https://www.landchina.com/default.aspx?tabid=263&ComName=default"
        self.host = "https://www.landchina.com/"
        # "https://www.landchina.com/default.aspx?tabid=386&comname=default&wmguid=75c72564-ffd9-426a-954b-8ac2df0903b7&recorderguid=9A6BC43332A33865E055000000000001"
        self.shortname = 'land_china'

    def __str__(self):
        return u"中国土地网"

    def get_src_url(self, *args):
        # logger.info("valid url=%s" % (self.url % key))
        return self.url

    def get_sub_urls(self, soup):
        # get all the urls showed in the info list page
        urls = []
        for i in soup.find_all('a'):
            url = i.get('href')
            if url is not None and url.startswith('default'):
                urls.append(url)

        urls = [self.host+x for x in urls]
        return urls
        # pass
    # def get_sub_full_urls(self, urllist):

    def get_target_info(self, soup):
        # get targe info from detail page
        #         # "https://www.landchina.com/default.aspx?tabid=386&comname=default&wmguid=75c72564-ffd9-426a-954b-8ac2df0903b7&recorderguid=9A6BC43332A33865E055000000000001"

        res = []
        r = soup.find_all('table', attrs={'id':'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1'})  # get empty
        for item in r:
            trs = item.find_all('tr')

            for tr in trs:
                tds= tr.find_all('td')
                # if len(tds) %2 ==0:

                if len(tds) % 2 != 0:
                    tds = tds[:-1]
                for i in list(range(len(tds)))[::2]:
                    # if len(re.findall('\d*.?\d*', tds[i].text)) == 0:
                    if len(tds[i].text) > 0:
                        res.append([tds[i].text, tds[i + 1].text])
                    # else:
        # logger.info("valid data length=%s" % (len(res)))
        return res
