# An example
class demo:
    _namespace = {}

    def __new__(cls, *args, **kwargs):
        obj = super(demo, cls).__new__(cls,*args, **kwargs)
        obj.__dict__ = obj._namespace
        return obj

d1 = demo()
d1.a = 'a'
d2 = demo() # d2 will have d2.a='a' when initiate
print(d2.a)

# all class inherit from demo() will share one _namespace
class child1(demo):
    pass

class child2(demo):
    pass

d1 = child1()
d1.a = 'aa'
d2 = child2()
print(d2.a)

# to avoid above behavior, to only apply this character to different classes
class demo1:
    _namespace = {}

    def __new__(cls, *args, **kwargs):
        obj = super(demo1, cls).__new__(cls,*args, **kwargs)
        obj.__dict__ = obj._namespace.setdefault(cls, {})
        return obj

class child1(demo1):
    pass

class child2(demo1):
    pass

d1 = child1()
d1.a = 'aa'
d2 = child2()
d2.b = 'bb'
d3 = child2()
print(d3.b)
# In above example, all instances of child1() share the same namespace, whereas all instances of child2() share a separate
# namespace

class Singleton:
   __instance = None
   @staticmethod
   def getInstance():
      """ Static access method. """
      if Singleton.__instance == None:
         Singleton()
      return Singleton.__instance
   def __init__(self):
      """ Virtually private constructor. """
      if Singleton.__instance != None:
         raise Exception("This class is a singleton!")
      else:
         Singleton.__instance = self
s = Singleton()
print(s)

s = Singleton.getInstance()
print(s)

s = Singleton.getInstance()
print(s)

# t = Singleton()
# the class can only call __init__() once , or will raise exception


#
def Singleton2(cls):
    _instance = {}
    def _singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    return _singleton

@Singleton2
class dem:
    def __init__(self, x):
        self.x = x

a1 = dem(1)
a2 = dem(2)
print(a1, a2)
print(a1.x, a2.x)