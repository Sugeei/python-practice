import pandas as pd


class Base:
    def __init__(self):
        print('Base')

class Borg:
    _namespace = {}
    # def __init__(self, *args, **kwargs):
        # self.__dict__ = Borg._namespace
        # print('Borg')

    def __new__(cls, *args, **kwargs):
        print('Borg')
        obj = super(Borg, cls).__new__(cls, *args, **kwargs)
        # obj.__dict__ = cls._namespace
        obj.__dict__ = cls._namespace.setdefault(cls, {})
        return obj

class Testing(Borg, Base):
    pass

a = Testing()
a.attr = 'abc'
print(a.attr)
a2 = Testing()
print(a2.attr)

class T2(Base, Borg):
    pass
#
# b = T2()
# b2 = T2()
# print(b.attr)
# # print(Borg())
#
# print(Base())

class demo(int):
    def __new__(cls, value):
        return super(demo, cls).__new__(cls, abs(value))

i = demo(-3)
print(i)

class A:
    def display(self):
        print('In Class A')

class B(A):
    def show(self):
        print('In Class B')


x = B()
x.display()

# Display MRO of Class B
print(B.mro())

class A:
    def display_x(self):
        print('In Class A')

class B(A):
    def display_y(self):
        print('In Class B')

class C(B):
    def display_z(self):
        print('In Class C')


x = C()
x.display_x()

# Display MRO of Class C
print(C.mro())

class A:
    def display_a(self):
        print('In Class A')

class B:
    def display_b(self):
        print('In Class B')

class C:
    def display_c(self):
        print('In Class C')

class X(A, B):
    def display_x(self):
        print('In Class X')

class Y(B, C):
    def display_y(self):
        print('In Class Y')

class Z(X, Y, C):
    def display_z(self):
        print('In Class Z')



x = Z()
x.display_a()

# Display MRO of Class Z
print(Z.mro())

Automatic Subclasses

import random
class Example:
    def __new__(cls, *args, **kwargs):
        cls = random.choice(cls.__subclasses__())
        return super(Example, cls).__new__(cls, *args, **kwargs)

class Spam(Example):
     pass

class Eggs(Example):
     pass

print(Example())
print(Example())
print(Example())
print(Example())
print(Example())