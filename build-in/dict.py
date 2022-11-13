
list = ['a', 'b']
pdict = dict.fromkeys(list)
pdict = dict.fromkeys(list, 0)



print(pdict)

b =[1,2]
# dict.fromkeys()
# print(dict.fromkeys(list, b))

pdict['c'] = 3
for k,v in zip(['c','d','e'], [4,5,6]):
    pdict[k] = v

d1 = {'a':1}
d2 = {'b':2, 'c':3}
for k, v in d2.items():
    d1[k] = v
print(d1)

d1.update(d2)
