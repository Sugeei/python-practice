class Date(object):

    print('cls start')
    def __init__(self, year=0, month=0, day=0):
        self.year = year
        self.month = month
        self.day = day

    @property
    def time(self):
        return "{year}-{month}-{day}".format(
            year=self.year,
            month=self.month,
            day=self.day
        )

    # 在 Date 内新增一个 classmethod
    @classmethod
    def from_string(cls, string):
        year, month, day = map(str, string.split('-'))
        # 在 classmethod 内可以通过 cls 来调用到类的方法，甚至创建实例
        date = cls(year, month, day)
        return date

    @classmethod
    def from_str(cls, strvar):
        year, month, day = map(str, strvar.split(' '))
        date =  cls(year, month, day)
        return date

    print('cls end')

def foo(x):
    print
    "executing foo(%s)" % (x)

class B(object):
    x = 20

    def __init__(self):
        self.x = 10
    def foo(self, x):
        print ("executing foo(%s,%s)" % (self, self.x))


    @classmethod
    def class_foo(cls, x):
        cls.x = 30
        print("executing class_foo(%s,%s)" % (cls, cls.x))

    @staticmethod
    def static_foo(x):
        print("executing static_foo(%s)" % x)

if __name__ == "__main__":
    a = B()
    a.foo(123)
    a.class_foo(234)
    a.static_foo(111)

    dateclass = Date(1999,1,1)
    print(dateclass.time)

    d2 = Date.from_str("1900 8 9")
    print(d2.time)

    d3 = Date(2999,1,1)
    print(d3.time)

