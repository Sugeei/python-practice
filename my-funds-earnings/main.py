# coding=utf8
import pandas as pd

# 交易记录， 主要是卖出记录
df = pd.read_csv('base-info.csv', dtype={'security-id':str})

# 持仓成本总额 成本*持有份额
df['hold-cost'] = df['cost-per-share'] * df['hold-share']
# 收益 总持有金额-持有成本
df['earnings'] = df['holdings'] - df['hold-cost']
df['share-earnings-ratio'] = (df['current-value-per-share'] - df['cost-per-share'])/ df['cost-per-share'] *100
print(df)

print("---------total earnings----------")
print(sum(df['earnings']))

