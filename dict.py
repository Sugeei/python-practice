# coding=utf-8
from collections import defaultdict

# https://www.accelebrate.com/blog/using-defaultdict-python/
# A defaultdict will never raise a KeyError
ice_cream = defaultdict(lambda: 'Vanilla')
ice_cream['Sarah'] = 'Chunky Monkey'
print(ice_cream["e"])
print(ice_cream["Sarah"])
for item, value in ice_cream.iteritems():
    print item, value

# In the following example, a defaultdict is used for counting.
food_list = 'spam spam spam spam spam spam eggs spam'.split()
food_count = defaultdict(int)  # default value of int is 0
for food in food_list:
    food_count[food] += 1  # increment element's value by 1
print dict(food_count)
#

# In the next example, we start with a list of states and cities. We want to build a dictionary where the keys are the state abbreviations and the values are lists of all cities for that state
city_list = [('TX', 'Austin'), ('TX', 'Houston'), ('NY', 'Albany'), ('NY', 'Syracuse'), ('NY', 'Buffalo'),
             ('NY', 'Rochester'), ('TX', 'Dallas'), ('CA', 'Sacramento'), ('CA', 'Palo Alto'), ('GA', 'Atlanta')]
cities_by_state = defaultdict(list)
for state, city in city_list:
    cities_by_state[state].append(city)
for state, cities in cities_by_state.iteritems():
    print state, ', '.join(cities)

a = range(10)
b = range(20)[10:]
for key, value in zip(a,b):
    print key, value
# # from collections import Counter
# from collections import defaultdict
#
# d = defaultdict(list)
# d["a"].insert(0, "test")
# print d
#
# s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
# d = defaultdict(list)
# for k, v in s:
#     d[k].append(v)
# print d.items()
#
# # https://docs.python.org/2/library/collections.html
# # print Counter([1, 1, 1, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]).most_common()
