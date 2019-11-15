def add(n, i):
    return n + i


def test():
    for i in range(4):
        yield i


g = test()

for n in [1, 10, 5, 3]:
    # for n in [1, 1]:
    g = (add(n, i) for i in g)

print(list(g))

# 所有的结果都是生成器表达式，不调用它，不从里面取值，就不干活。附上我的推导过程

# 意思是在没调用之前都是一堆表达式， 调用的时候发现n的值是多少，就全拿那个值算
# 那么相当于要循环多少次就有多少个惰性生成器在waiting, 调用后的结果就是最后n的值按次数加倍
