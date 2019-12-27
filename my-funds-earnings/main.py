# coding=utf8
import pandas as pd

# 交易记录， 主要是卖出记录
alldf = pd.read_csv('base-info.csv', dtype={'security-id':str})
for k, df in alldf.groupby('trade_date'):

    # 持仓成本总额 成本*持有份额
    df['hold-cost'] = df['cost-per-share'] * df['hold-share']
    # 收益 总持有金额-持有成本
    df['earnings'] = df['holdings'] - df['hold-cost']
    df['share-earnings-ratio'] = (df['current-value-per-share'] - df['cost-per-share'])/ df['cost-per-share'] *100
    print(df)

    print("---------total earnings %s----------" % k)
    print(sum(df['earnings']))

    #
    # # 读取卖出信息， 统计净收益
    # df = pd.read_csv('sellings.csv', dtype={'security-id':str})
    # df['net-earnings'] = df['out-value'] - df['cost-per-share'] * df['out-share']
    # print(df)
    # print("---------total net earnings----------")
    # print(sum(df['net-earnings']))
