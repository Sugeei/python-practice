# to see vesion of a module
# pandas.__version__

# 字典合并
x = {'x': 1, 'y': 2}
y = {'a': 3, 'b': 4}
z = {**x, **y}
print(z)

a = set(range(10))
b = set(range(15))
# 交集
print(a & b)
# 差集
print(list(a ^ b))
# 并集
print(list(a | b))


# tuple
# >>> import numpy as np
# >>> a = np.nan
# >>> tuple(a)
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# TypeError: 'float' object is not iterable
# >>> a = [np.nan]
# >>> tuple(a)
# (nan,)
# >>>


# TODO how to avoid python tuple converting np.nan to string nan
# https://stackoverflow.com/questions/14162723/replacing-pandas-or-numpy-nan-with-a-none-to-use-with-mysqldb
# TODO why df.where((pd.notnull(df)), None) is not working
# https://stackoverflow.com/questions/17534106/what-is-the-difference-between-nan-and-none
# Not-A-Number
# After years of production use [NaN] has proven, at least in my opinion, to be the best decision given the state of affairs in NumPy and Python in general. The special value NaN (Not-A-Number) is used everywhere as the NA value, and there are API functions isnull and notnull which can be used across the dtypes to detect NA values.
# ...
# Thus, I have chosen the Pythonic “practicality beats purity” approach and traded integer NA capability for a much simpler approach of using a special value in float and object arrays to denote NA, and promoting integer arrays to floating when NAs must be introduced.
# https://pandas-docs.github.io/pandas-docs-travis/user_guide/missing_data.html
# One has to be mindful that in Python (and NumPy), the nan's don’t compare equal, but None's do. Note that pandas/NumPy uses the fact that np.nan != np.nan, and treats None like np.nan.


# Say I have a list
fruits = ["apple", "orange", "banana", "lemon"]
# I try to figure out whether a given character like "p" exists in one of these elements
if any("p" in element for element in fruits):
    print("yes")
else:
    print("failed")

# If I want to know whether "a" can be found in all these elements
if all("p" in element for element in fruits):
    print("yes")
else:
    print("failed")

print(any([]))
