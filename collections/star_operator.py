# coding=utf-8

# * operator
# https://docs.python.org/2/library/collections.html

from collections import Counter
from collections import defaultdict
from collections import namedtuple

d = defaultdict(list)
d["a"].insert(0, "test")

# print d

print(Counter([1, 1, 1, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]).most_common())

c = Counter(a=4, b=2, c=0, d=-2)
print(c + Counter())
