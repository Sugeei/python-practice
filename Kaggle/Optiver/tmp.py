import pandas as pd
# from pandas import read_parquet
import pyarrow.parquet as pq
import datacompy
a = ['a','b','c']
b = ['a','b','c']
print(a == b)
da = pd.DataFrame(columns=['t'])
da.loc[0, 't'] = a
da.reset_index(inplace=True)
db = pd.DataFrame(columns=['t'])
db.loc[0, 't'] = b
db.reset_index(inplace=True)
print(db.columns)
print(da==db)

print(datacompy.Compare(da,db, ['index','t']).matches())
print(datacompy.Compare(da,db, ['index','t']).report())
# df = pq.ParquetFile("c439ef22282f412ba39e9137a3fdabac.parquet.zip")
# df = pd.read_parquet("trade_train.parqueet.zip")
# print(df)