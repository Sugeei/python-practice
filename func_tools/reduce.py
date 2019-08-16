from functools import reduce
# 内层函数待到调用的时候才执行
def lazy_sum(arr):
    def sum_sum():
        print("1")
        return reduce(lambda x, y: x + y, arr)
    return sum_sum
l = [1, 2, 3, 4, 5]


def rolling_sum(i):
    return sum(l[0:i+1])
print(list(map(rolling_sum, range(len(l)))))


f = lazy_sum([1, 2, 3, 4, 5])
