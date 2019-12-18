# createMetaclass create Classes and Classes creates objects
# https://www.geeksforgeeks.org/metaprogramming-metaclasses-python/

# To create our custom metaclass, our custom metaclass have to inherit type metaclass and usually override –
#
# __new__(): It’s a method which is called before __init__(). It creates the object and return it. We can overide this method to control how the objects are created.
# __init__(): This method just initialize the created object passed as parameter

class SingletonMetaclass(type):
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super(SingletonMetaclass, self).__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance


#
# 作者：浮生若梦的编程
# 链接：https://juejin.im/post/5a64255c51882573432d42e0
# 来源：掘金
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。


class Single():
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super(Single, self).__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance


class SingletonDecorator:
    def __init__(self, klass):
        self.klass = klass
        self.instance = None

    def __call__(self, *args, **kwds):
        if self.instance is None:
            self.instance = self.klass(*args, **kwds)
        return self.instance


@SingletonDecorator
class Demo():
    pass
