# fancy =   factors:3,5,7  1, 3, 5, 7, 9, 15, 21, 25, 27, 35,

# [1]
# [1] * [3 5 7] min() -> [1 3]
# [1 3] * [3 5 7] min() -> [1 3 5]
# [1 3 5] *
#

input = 6
output = 15

class solution():
    def fancynumber(self, x):
        if x == 1:
            return 1
        fancylist = [1,3,5,7]

        while x > len(fancylist):
            l = len(fancylist)

            tmp = [v for v in fancylist]

            for val in tmp:
                # fancylist.append(max([val * e for e in [3,5,7]]))
                fancylist.extend([val * e for e in tmp])
            fancylist = list(set(fancylist))

            fancylist.sort()
            fancylist = fancylist[:l+1]
            print(fancylist)

        return fancylist[x-1]

    def fancy(self, x):
        fancylist = [1]
        while x > len(fancylist):
            l = fancylist[-1]
            newelem = 0
            while newelem == 0:
                l +=1
                if l%3 == 0:
                    pass

        return fancylist[x-1]
print(solution().fancynumber(70))

#
# fixed income
# derivative option swap future
# risk system
# yield curve
# price change
# china trading system

divmod(8, 4)

from collections import namedtuple

divmod(8, 4)

def custom_divmod(a, b):
    DivMod = namedtuple("DivMod", "quotient remainder")
    return DivMod(*divmod(a, b))

custom_divmod(8, 4)
# DivMod(quotient=2, remainder=0)

from math import sqrt
print(sqrt(0.5 * 2) -1  )

