class base():
    val = 10

    def foo(self):
        print(self.val)


class child(base):
    def f(self):
        self.val = 20
        self.foo()


class child2(base):
    def f(self):
        print(self.val)


ins = child()
ins.f()

ins2 = child2()
ins2.f()

# child, child2各自继承自base, 相当于复制， child对val做的修改只对自己有效