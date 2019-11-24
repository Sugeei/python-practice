class Employee:

    def __init__(self, fullname, age, income):
        self.fullname = fullname
        self.age = age
        self.income = income

    def func_information(self):
        print('At age', self.age, self.fullname, 'is earning', self.income)


class Department(Employee):

    def __init__(self, fullname, age, income):
        # Employee.__init__(self, fullname, age, income)
        super(Department, self).__init__(fullname, age, income)
        # 注意super的语法
emp = Employee('John', '27', '650000')
emp.func_information()

print('--------------')
dept = Department('Jenny', '25', '850005')
print(dept.fullname)
dept.func_information()
