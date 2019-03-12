# coding=utf-8
#  ```

# Python的闭包是延迟绑定(late binding)的。
# 这表明在闭包中使用的变量直到内层函数被调用的时候才会被查找。
# 结果是，当调用multipliers()返回的函数时，i参数的值会在这时被在调用环境中查找。
# 所以，无论调用返回的哪个函数，for循环此时已经结束，i等于它最终的值3。
# 因此，所有返回的函数都要乘以传递过来的3，因为上面的代码传递了2作为参数，所以他们都返回了6（即，3 * 2）

# 正如在书《The Hitchhiker’s Guide to Python》中提出来的一样,
# 有一种广泛传播的误解认为这个问题和lambda表达式有关，事实并非如此。
# 通过lambda表达式产生的函数并没有什么特别之处，使用普通的def定义的函数的行为和lambda表达式产生的函数的行为是一样的
origin = [0, 0]  # 坐标系统原点
legal_x = [0, 50]  # x轴方向的合法坐标
legal_y = [0, 50]  # y轴方向的合法坐标


# 闭包 希望函数的每次执行结果，都是基于这个函数上次的运行结果
# https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Closures
# https://www.jb51.net/article/54498.htm
def create(pos=origin):
    def player(direction, step):
        # 这里应该首先判断参数direction,step的合法性，比如direction不能斜着走，step不能为负等
        # 然后还要对新生成的x，y坐标的合法性进行判断处理，这里主要是想介绍闭包，就不详细写了。
        new_x = pos[0] + direction[0] * step
        new_y = pos[1] + direction[1] * step
        pos[0] = new_x
        pos[1] = new_y
        # 注意！此处不能写成 pos = [new_x, new_y]，原因在上文有说过
        return pos

    return player


player = create()  # 创建棋子player，起点为原点
print player([1, 0], 10)  # 向x轴正方向移动10步
print player([0, 1], 20)  # 向y轴正方向移动20步
print player([-1, 0], 10)  # 向x轴负方向移动10步


def multipliers():
    return [lambda x: i * x for i in range(4)]


print [m(2) for m in multipliers()]


# 可以绕过这个问题的方法。
# 方法一是像下面一样使用Python的生成器(generator)
def multipliers2():
    for i in range(4): yield lambda x: i * x


print [m(2) for m in multipliers2()]

# 也可以使用functools.partial函数
from functools import partial
from operator import mul


def multipliers():
    return [partial(mul, i) for i in range(4)]


from functools import reduce


# 内层函数待到调用的时候才执行
def lazy_sum(arr):
    def sum_sum():
        print("1")
        return reduce(lambda x, y: x + y, arr)
    return sum_sum


f = lazy_sum([1, 2, 3, 4, 5])

print reduce(lambda x, y: x + y, [1, 2, 3, 4, 5])
print f()
