# createMetaclass create Classes and Classes creates objects
# https://www.geeksforgeeks.org/metaprogramming-metaclasses-python/

# To create our custom metaclass, our custom metaclass have to inherit type metaclass and usually override –
#
# __new__(): It’s a method which is called before __init__(). It creates the object and return it. We can overide this method to control how the objects are created.
# __init__(): This method just initialize the created object passed as parameter

class SingletonMetaclass(type):
    __instance = {}
    #
    # def __init__(self, *args, **kwargs):
    #     if SingletonMetaclass.__instance is None:
    #         SingletonMetaclass.__instance = SingletonMetaclass()

    def __call__(cls):
        if cls not in cls.__instance:
            cls.__instance[cls]  = super(SingletonMetaclass, cls).__call__()
        return cls.__instance[cls]
        # self.__instance = None
        # super().__init__(*args, **kwargs)
    #
    # def __call__(self, *args, **kwargs):
    #     if self.__instance is None:
    #         self.__instance = SingletonMetaclass()
    #         return self.__instance
    #     else:
    #         return self.__instance__
#
# 作者：浮生若梦的编程
# 链接：https://juejin.im/post/5a64255c51882573432d42e0
# 来源：掘金
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。


# s = SingletonMetaclassss()
#
# t = SingletonMetaclass()
class Demo(metaclass=SingletonMetaclass):
    pass

a= Demo()
b= Demo()

print(a==b)

# https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python