# coding=utf8
import pandas as pd

df = pd.read_csv('base-info.csv', dtype={'security-id':str})

# 持仓成本总额 成本*持有份额
df['hold-cost'] = df['cost-per-share'] * df['hold-share']
# 收益 总持有金额-持有成本
df['earnings'] = df['holdings'] - df['hold-cost']
df['share-earnings-ratio'] = (df['current-value-per-share'] - df['cost-per-share'])/ df['cost-per-share'] *100
print(df)

print("---------total earnings----------")
print(sum(df['earnings']))


df = pd.read_csv('sellings.csv', dtype={'security-id':str})
df['net-earnings'] = df['out-value'] - df['cost-per-share'] * df['out-share']
print(df)
print("---------total net earnings----------")
print(sum(df['net-earnings']))
