import pandas as pd

df = pd.read_csv('train.csv')

print(id(df))

d = {"key": df}

df2 = d['key'].copy() # new memory

df4=d['key']
print(id(df2))
print(id(df4))
print(id(df)==id(df4))

df3 = df2[df2.Individual ==19]

print(id(df3))

