# coding=utf-8

# inheritance
# overridding

class Person():
    def __init__(self, first, last, age):
        self.firstname = first
        self.lastname = last
        self.age = age

    def __str__(self):
        return self.firstname + " " + self.lastname + ", " + str(self.age)


class Employee(Person):
    def __init__(self, first, last, age, staffnum):
        Person.__init__(self, first, last, age)
        self.staffnumber = staffnum

    def __str__(self):
        return Person.__str__(self) + ", " + self.staffnumber


x = Person("Marge", "Simpson", 36)
y = Employee("Homer", "Simpson", 28, "1007")

print(x)
print(y)
