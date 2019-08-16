from tree.traverse import Forest
# import
import os

dir = os.path.dirname(os.path.realpath(__file__))
dependenceforest = Forest()
dependenceforest.build_from(os.path.join(dir, 'factors_dependence.json'))
dependenceforest.preorder_traverse()

print(dependenceforest.path_to('cashconversioncycle') ==[u'accountspayablestrate', u'accountspayablestdays'])
print(dependenceforest.path_to('cashconversioncycle'))
print(dependenceforest.path_to('bias20') ==["ma20"])
print(dependenceforest.path_to('bias20'))
print(dependenceforest.path_to('a')==[u'e', u'c', u'd', u'b'])
print(dependenceforest.path_to('a'))
# "cashconversioncycle")