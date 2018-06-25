# -*- coding: utf-8 -*-
# https://www.zhihu.com/question/29648560
# https://wenku.baidu.com/view/aed699ceb9d528ea81c779e2?pcf=2#2
# https://www.joinquant.com/data/dict/fundamentals
import urllib
import datetime

# 获取指定股票的所有历史数据
def download_stock_data(stock_list):
    for sid in stock_list:
        url = "http://table.finance.yahoo.com/table.csv?s=" + sid
        frame = sid + ".csv"
        print("downloading %s from %s" % (frame, url))
        urllib.urlretrieve(url, frame)

# 获取某个时间段指定股票数据
def download_stock_data_in_period(stock_list, start, end):
    for sid in stock_list:
        params = {"a": start.month - 1, "b": start.day, "c": start.year,
                  "d": end.month - 1, "e": end.day, "f": end.year, "s": sid}
        url = "http://table.finance.yahoo.com/table.csv?"
        qs = urllib.urlencode(params)
        url = url + qs
        frame = "%s_%d%d%d_%d%d%d.csv" % (sid, start.year, start.month, start.day,
                                          end.year, end.month, end.day)
        print("downloading %s from %s" % (frame, url))
        urllib.urlretrieve(url, frame)


if __name__ == "__main__":
    stock_list = ["300001.sz"]
    start = datetime.date(year=2015, month=11, day=17)
    end = datetime.date(year=2015, month=12, day=17)
    download_stock_data(stock_list)
    download_stock_data_in_period(stock_list, start, end)