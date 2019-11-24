def factorial(v):
    if v == 0:
        # if v == 0 or v == 1:
        return 1
    else:
        return (v * factorial(v - 1))


# print(factorial(5))


def b(n, k):
    if k > n:
        return -1
    if k < 0:
        return -1
    r = factorial(n) / (factorial(k) * factorial(n - k))
    if r > 1000000000:
        return -1
    else:
        return int(r)


# print(b(40, 20))
# print(b(3, 5))
# print(b(5, 3))


def m(l):
    lm = max(l)
    lmin = min(l)
    if lmin <=0:
        return 1
    ref = set(range(1, lm + 1))
    diff = list(set(l) ^ ref)
    if len(diff) > 0:
        return diff[0]
    elif lmin > 0:
        return lm + 1
    # else:
    #     return 1


print(m([6, 4, 2]))
print(m([1, 2, 3]))
print(m([1, 3, 6, 4, 1, 2]))
print(m([-1, -3]))
