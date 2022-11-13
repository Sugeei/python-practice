# class DictionaryRecord:
#     def __init__(self, data):
#         self._data = data
#
#     # def __getattr__(self, name):
#     #     print('call __getattr__')
#     #     result = self._data
#     #     if name not in result.keys():
#     #         self._data[name] = 1
#     #     return result[name]
#
#     def __getattribute__(self, name):
#         print('call _getattribute__{name!r}', name)
#         data_dict = super().__getattribute__('_data')
#         # if name not in data_dict.keys():
#         #     self._data[name] = 1
#         return data_dict[name]
#
# data = DictionaryRecord({'foo':3})
# print('foo: ', data.foo)
# print('moo: ', data.moo)
# print('moo: ', data.moo)
#
class Employee:
    def __init__(self):
        self.position = "a"
        self._position = 'b'

    @property
    def position(self):
        print("Get Employee Position: ")
        return self._position

    @position.setter
    def position(self, value):
        print("Set Position")
        self._position = value


Jacob = Employee()
Jinku = Employee()
print(dir(Jacob))
print(Jacob.position)

Jacob.position = "Engineer II"
Jinku.position = "Senior Engineer"

print(Jacob.position)
print(Jinku.position)

class A:
    def __init__(self):
        self.__private()
        self.public()
    def __private(self):
        print("A.__private()")
    def public(self):
        print("A.public()")

class B(A):
    def __private(self):
        print("B.__private()")
    def public(self):
        print("B.public()")

b=B()

value=0
if value:
    print(True)
else:
    print(False)

# 双下划线的另一个重要的目地是，避免子类对父类同名属性的冲突
# 当实例化B的时候，由于没有定义_ _ init_ 函数，将调用父类的 _ init_ _，但是由于双下划线的"混淆"效果，"self.__private()"将变成 “self._A__private()”。
form =1
is_valid = form is not None & form.is_valid(True)
is_valid = form is not None and form.is_valid(include_hidden_fields=True)
# greater insight into its purpose

is_dict = {}

value = 0
if value is not None and value !="":
    pass
if value:
    pass

"""



"""
# Designing frameworks can be a very complicated process;
# programmers are ofter expected to specify a variety of different types of information.

class SuppressErrors:
    def __init__(self, *exceptions):
        if not exceptions:
            print('not exception')
            exceptions = (Exception,)
        self.exceptions = exceptions

    def __enter__(self):
        pass

    def __exit__(self, exc_class, exc_instance, traceback):
        print(exc_instance)
        print(self.exceptions)
        if isinstance(exc_instance, self.exceptions):
            return True
        return False


print(1)
with SuppressErrors():
    1 / 0
print(2)
with SuppressErrors(IndexError):
    a = [1, 2, 3]
    print(a[4])
print(3)
with SuppressErrors(KeyError):
    a = [1, 2, 3]
    print(a[4])