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