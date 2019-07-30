# coding=utf-8

# * operator

from collections import Counter
from collections import defaultdict


d = defaultdict(list)
d["a"].insert(0, "test")

# print d

print(Counter([1,1,1,2,2,2,2,2,2,4,4,4,4,4,6,6,6,6,6,6,6,6,6,6,6]).most_common())

