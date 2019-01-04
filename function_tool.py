import functools

my_list = [1, 2, 3, 4, 5]


def add_it(x, y):
    return (x + y)


sum = functools.reduce(add_it, my_list)
print(sum)

sum = functools.reduce(lambda x, y: x + y, range(101))
print sum
