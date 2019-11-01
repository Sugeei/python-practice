# 读文件， yield分块读， 完了再分ticker存储到不同子文件
import pandas as pd
import os

import time


def decorator_timecount(func):
    def subfun(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        print("time consumed for func %s is %s " % (func.__name__, int(time.time() - t1)))
        # print("time consumed for func %s is %s " % (func.__name__, int(time.time() - t1)))
        return result

    return subfun


def read_block(fpath):
    block_size = 1024
    with open(fpath, 'rb') as f:
        while True:
            block = f.read(block_size)
            if block:
                yield block
            else:
                return


def read_head(fpath):
    block_size = 1024
    with open(fpath, 'r') as f:
        head = f.readline()
        columns = head.strip().split(',')
    return columns


def read_row(fpath):
    with open(fpath, 'r') as f:
        i = 0
        row = f.readline()

        while True:
            row = f.readline()
            # if i == 0:
            #     continue
            if row:
                yield row
            else:
                return i
            i += 1


from collections import defaultdict


class TickerSpliter():
    def __init__(self, fpath):
        self.ticker_collector = defaultdict(list)
        self.tickers = set()
        self.title = None
        self.fpath = fpath
        self.targetdir = None

    def head(self):
        columns = read_head('true.csv')
        self.targetdir = '2019-11-03'
        self.title = columns

    @decorator_timecount
    def split(self):
        self.head()
        for content in read_row('true.csv'):
            value = content.strip().split(',')
            ticker = value[1]
            self.ticker_collector[ticker].append(value)

    @decorator_timecount
    def write(self):
        """
        time consumed for func write is 213
        :return:
        """
        if not os.path.exists(self.targetdir):
            os.mkdir(self.targetdir)
        for ticker, value in self.ticker_collector.items():
            df = pd.DataFrame(self.ticker_collector[ticker], columns=self.title)
            df.to_csv(os.path.join(self.targetdir, '%s.csv' % ticker))

    @decorator_timecount
    def split_and_write(self):
        """
        time consumed for func split_and_write is 464
        :return:
        """
        tickerspliter.head()
        if not os.path.exists(self.targetdir):
            os.mkdir(self.targetdir)
        for content in read_row(self.fpath):
            df = pd.DataFrame([content.strip().split(',')], columns=self.title)
            ticker = df.loc[0, "ticker_symbol"]
            if ticker not in self.tickers:
                with open(os.path.join(self.targetdir, '%s.csv' % ticker), 'a') as f:
                    f.write(','.join(self.title))
                    f.write('\n')
                self.tickers.add(ticker)
            with open(os.path.join(self.targetdir, '%s.csv' % ticker), 'a') as f:
                f.write(','.join(df.values.tolist()[0]))
                f.write('\n')
            # print(content)


tickerspliter = TickerSpliter('true.csv')

# The first way
tickerspliter.split_and_write()

# The second way
tickerspliter.split()
tickerspliter.write()
