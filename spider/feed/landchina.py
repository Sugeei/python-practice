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

"""
Request URL: https://www.landchina.com/default.aspx?tabid=263&ComName=default
Request Method: POST
Status Code: 200 OK
Remote Address: 218.246.22.166:443
Referrer Policy: no-referrer-when-downgrade
Cache-Control: private
Connection: keep-alive
Content-Encoding: gzip
Content-Type: text/html; charset=gb2312
Date: Wed, 01 Jan 2020 08:45:35 GMT
Server: nginx
Transfer-Encoding: chunked
X-AspNet-Version: 4.0.30319
X-Powered-By: ASP.NET
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7
Cache-Control: max-age=0
Connection: keep-alive
Content-Length: 3126
Content-Type: application/x-www-form-urlencoded
Cookie: ASP.NET_SessionId=u40njztxvyi3vx1oqkekyvlh; Hm_lvt_83853859c7247c5b03b527894622d3fa=1577495498; security_session_verify=f828e2cb1e965d40d50132dcf77f18e1; security_session_mid_verify=7d8ff7d5461c22d06d0a48116828399e; Hm_lpvt_83853859c7247c5b03b527894622d3fa=1577868234
Host: www.landchina.com
Origin: https://www.landchina.com
Referer: https://www.landchina.com/default.aspx?tabid=263&ComName=default
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36
tabid: 263
ComName: default
__VIEWSTATE: /wEPDwUJNjkzNzgyNTU4D2QWAmYPZBYIZg9kFgICAQ9kFgJmDxYCHgdWaXNpYmxlaGQCAQ9kFgICAQ8WAh4Fc3R5bGUFIEJBQ0tHUk9VTkQtQ09MT1I6I2YzZjVmNztDT0xPUjo7ZAICD2QWAgIBD2QWAmYPZBYCZg9kFgJmD2QWBGYPZBYCZg9kFgJmD2QWAmYPZBYCZg9kFgJmDxYEHwEFIENPTE9SOiNEM0QzRDM7QkFDS0dST1VORC1DT0xPUjo7HwBoFgJmD2QWAgIBD2QWAmYPDxYCHgRUZXh0ZWRkAgEPZBYCZg9kFgJmD2QWAmYPZBYEZg9kFgJmDxYEHwEFhwFDT0xPUjojRDNEM0QzO0JBQ0tHUk9VTkQtQ09MT1I6O0JBQ0tHUk9VTkQtSU1BR0U6dXJsKGh0dHA6Ly93d3cubGFuZGNoaW5hLmNvbS9Vc2VyL2RlZmF1bHQvVXBsb2FkL3N5c0ZyYW1lSW1nL3hfdGRzY3dfc3lfamhnZ18wMDAuZ2lmKTseBmhlaWdodAUBMxYCZg9kFgICAQ9kFgJmDw8WAh8CZWRkAgIPZBYCZg9kFgJmD2QWAmYPZBYCZg9kFgJmD2QWAmYPZBYEZg9kFgJmDxYEHwEFIENPTE9SOiNEM0QzRDM7QkFDS0dST1VORC1DT0xPUjo7HwBoFgJmD2QWAgIBD2QWAmYPDxYCHwJlZGQCAg9kFgJmD2QWBGYPZBYCZg9kFgJmD2QWAmYPZBYCZg9kFgJmD2QWAmYPFgQfAQUgQ09MT1I6I0QzRDNEMztCQUNLR1JPVU5ELUNPTE9SOjsfAGgWAmYPZBYCAgEPZBYCZg8PFgIfAmVkZAICD2QWBGYPZBYCZg9kFgJmD2QWAmYPZBYCAgEPZBYCZg8WBB8BBYYBQ09MT1I6I0QzRDNEMztCQUNLR1JPVU5ELUNPTE9SOjtCQUNLR1JPVU5ELUlNQUdFOnVybChodHRwOi8vd3d3LmxhbmRjaGluYS5jb20vVXNlci9kZWZhdWx0L1VwbG9hZC9zeXNGcmFtZUltZy94X3Rkc2N3X3p5X2pnZ2dfMDEuZ2lmKTsfAwUCNDYWAmYPZBYCAgEPZBYCZg8PFgIfAmVkZAIBD2QWAmYPZBYCZg9kFgJmD2QWAgIBD2QWAmYPFgQfAQUgQ09MT1I6I0QzRDNEMztCQUNLR1JPVU5ELUNPTE9SOjsfAGgWAmYPZBYCAgEPZBYCZg8PFgIfAmVkZAIDD2QWAgIDDxYEHglpbm5lcmh0bWwF/AY8cCBhbGlnbj0iY2VudGVyIj48c3BhbiBzdHlsZT0iZm9udC1zaXplOiB4LXNtYWxsIj4mbmJzcDs8YnIgLz4NCiZuYnNwOzxhIHRhcmdldD0iX3NlbGYiIGhyZWY9Imh0dHBzOi8vd3d3LmxhbmRjaGluYS5jb20vIj48aW1nIGJvcmRlcj0iMCIgYWx0PSIiIHdpZHRoPSIyNjAiIGhlaWdodD0iNjEiIHNyYz0iL1VzZXIvZGVmYXVsdC9VcGxvYWQvZmNrL2ltYWdlL3Rkc2N3X2xvZ2UucG5nIiAvPjwvYT4mbmJzcDs8YnIgLz4NCiZuYnNwOzxzcGFuIHN0eWxlPSJjb2xvcjogI2ZmZmZmZiI+Q29weXJpZ2h0IDIwMDgtMjAxOSBEUkNuZXQuIEFsbCBSaWdodHMgUmVzZXJ2ZWQmbmJzcDsmbmJzcDsmbmJzcDsgPHNjcmlwdCB0eXBlPSJ0ZXh0L2phdmFzY3JpcHQiPg0KdmFyIF9iZGhtUHJvdG9jb2wgPSAoKCJodHRwczoiID09IGRvY3VtZW50LmxvY2F0aW9uLnByb3RvY29sKSA/ICIgaHR0cHM6Ly8iIDogIiBodHRwczovLyIpOw0KZG9jdW1lbnQud3JpdGUodW5lc2NhcGUoIiUzQ3NjcmlwdCBzcmM9JyIgKyBfYmRobVByb3RvY29sICsgImhtLmJhaWR1LmNvbS9oLmpzJTNGODM4NTM4NTljNzI0N2M1YjAzYjUyNzg5NDYyMmQzZmEnIHR5cGU9J3RleHQvamF2YXNjcmlwdCclM0UlM0Mvc2NyaXB0JTNFIikpOw0KPC9zY3JpcHQ+Jm5ic3A7PGJyIC8+DQrniYjmnYPmiYDmnIkmbmJzcDsg5Lit5Zu95Zyf5Zyw5biC5Zy6572RJm5ic3A7Jm5ic3A75oqA5pyv5pSv5oyBOua1meaxn+iHu+WWhOenkeaKgOiCoeS7veaciemZkOWFrOWPuCZuYnNwOzxiciAvPg0K5aSH5qGI5Y+3OiDkuqxJQ1DlpIcwOTA3NDk5MuWPtyDkuqzlhaznvZHlronlpIcxMTAxMDIwMDA2NjYoMikmbmJzcDs8YnIgLz4NCjwvc3Bhbj4mbmJzcDsmbmJzcDsmbmJzcDs8YnIgLz4NCiZuYnNwOzwvc3Bhbj48L3A+HwEFZEJBQ0tHUk9VTkQtSU1BR0U6dXJsKGh0dHA6Ly93d3cubGFuZGNoaW5hLmNvbS9Vc2VyL2RlZmF1bHQvVXBsb2FkL3N5c0ZyYW1lSW1nL3hfdGRzY3cyMDEzX3l3XzEuanBnKTtkZM3NvnlXlCHsxkc6av00AJnK3vbhmjQCCXm5QkCZwr58
__EVENTVALIDATION: /wEdAAIo20rirRFW2+eFhO6+Mw9qCeA4P5qp+tM6YGffBqgTjTZh/IuwdhzpiegZclaPF5waXsY9AwQQV7PLcCma+lPB
hidComName: default
TAB_QueryConditionItem: 9f2c3acd-0256-4da2-a659-6949c4671a2a
TAB_QuerySortItemList: 282:False
TAB_QuerySubmitConditionData: 9f2c3acd-0256-4da2-a659-6949c4671a2a:2018-11-1~
TAB_QuerySubmitOrderData: 282:False
TAB_RowButtonActionControl:
TAB_QuerySubmitPagerData: 2
TAB_QuerySubmitSortData:
"""