# 读文件， yield分块读， 完了再分ticker存储到不同子文件
import pandas as pd


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

#
# i = 0
# columns = read_head('true.csv')
# tragetpath = '2019-11-01'
# import os
#
# if not os.path.exists(tragetpath):
#     os.mkdir(tragetpath)
# for content in read_row('true.csv'):
#     # if i == 0:
#     #     第一次取出表头
#     #     lines = content.splitlines()
#     df = pd.DataFrame([content.strip().split(',')], columns=columns)
#     ticker = df.loc[0, "ticker_symbol"]
#     with open(os.path.join(tragetpath, '%s.csv' % ticker), 'a') as f:
#         f.write(','.join(df.values.tolist()[0]))
#         f.write('\n')
#     # print(content)

def fun_inner():
    i = 0
    while True:
        i = yield i

def fun_outer():
    yield from fun_inner()


def sample_generator(i):
    for j in range(i):
        yield j

print(list(sample_generator(5)))

for value in sample_generator(5):
    print(value)

if __name__ == '__main__':
    outer = fun_outer()
    outer.send(None)
    for i in range(5):
        print(outer.send(i))