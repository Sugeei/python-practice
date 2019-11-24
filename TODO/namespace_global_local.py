# global i
i = 1  # 全局作用域


def f():
    # i = 0
    i += 1  # 局部作用域
    print(i)


f()
print(i)
