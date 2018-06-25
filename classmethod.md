```
def f(x,l=[]):

for i in range(x):

l.append(i*i)

print (l)

f(2)

f(3,[3,2,1])

f(3)

```

```

>>>

[0, 1]

[3, 2, 1, 0, 1, 4]

[0, 1, 0, 1, 4] # 使用了第一次调用时存储的旧列表。python2.7. why

>>>

```



>做到了支持封闭性与扩展性

工厂模式

http://pythoncentral.io/difference-between-staticmethod-and-classmethod-in-python/

Meaning of @classmethod and @staticmethod for beginner?https://stackoverflow.com/questions/12179271/meaning-of-classmethod-and-staticmethod-for-beginner


# The difference between @classmethod and @staticmethod
- classmethod can be used to provide another init method for class
- classmethod defines a function that should be ihnerited by subclasses
- static method
