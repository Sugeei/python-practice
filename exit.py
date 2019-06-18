class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __enter__(self):
        print("in __enter__")
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        # class 异常退出时调用此函数
        print("in __exit__ %s %s " % (self.width, self.height))

    def divide_by_zero(self):
        # causes ZeroDivisionError exception
        return self.width / 0


with Rectangle(3, 4) as r:
    # exception successfully pass to __exit__
    r.divide_by_zero()


# Output:
# "in __enter__"
# "in __exit__"
# Traceback (most recent call last):
#   File "e0235.py", line 27, in <module>
#     r.divide_by_zero()
