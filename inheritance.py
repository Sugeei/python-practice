# coding=utf-8

# inheritance
# overridding
# https://www.python-course.eu/python3_inheritance.php
# Overriding means that the first definition is not available anymore.
# In C++, Having a function with a different number of parameters is another way of function overloading.
#
# base
class Person():
    count = 0

    def __init__(self, first, last, age):
        type(self).count += 1
        self.firstname = first
        self.lastname = last
        self.age = age

    def __str__(self):
        return self.firstname + " " + self.lastname + ", " + str(self.age)

    def __del__(self):
        type(self).count -= 1

    @staticmethod
    def personcount():
        """
        https://www.python-course.eu/python3_class_and_instance_attributes.php
        :return:
        """
        return Person.count

    def word(self):
        print("my firstname is %s" % self.firstname)


# TODO how to count the instances
# inherit Person
class Employee(Person):
    def __init__(self, first, last, age, staffnum):
        Person.__init__(self, first, last, age)
        self.id = Person.count + 1
        Person.count += 1
        self.staffnumber = staffnum

    def __str__(self):
        return Person.__str__(self) + ", " + self.staffnumber

    def word(self):
        print("sub class employee ")


x = Person("Marge", "Simpson", 36)
y = Employee("Homer", "Simpson", 28, "1007")

print(x)
print(y)

x.word()
y.word()
#########################################################################

# 在python中，类中的变量在内部被当作字典处理。
# 如果一个变量名在当前类的字典中没有被发现，
# 系统将会在这个类的祖先(例如，它的父类)中继续寻找，
# 直到找到为止(如果一个变量名在这个类和这个类的祖先中都没有，那么将会引发一个AttributeError错误)

# 因此，在父类中将变量x赋值为1，那么x变量将可以被当前类和所有这个类的子类引用。这就是为什么第一个print语句输出为1 1 1.
#
# 接下来，如果它的子类覆盖了这个值(例如， 当我们执行Child1.x = 2)，那么这个变量的值仅仅在这个子类中发生了改变。
# 这就是为什么第二个print语句输出1 2 1
#
# 最后，如果父类改变了这个变量的值(例如，我们执行Parent.x = 3)，
# 所有没有覆盖这个参数值的子类(在这个例子中覆盖了参数的就是Child2)都会受到影响，
# 这就是为什么第三个print语句的输出为3 2 3
