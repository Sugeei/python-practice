class base():
    val = 10

    def foo(self):
        print(self.val)


class child(base):
    def f(self):
        base.val +=1
        self.foo()


class child2(base):
    def f(self):
        print(self.val)
        print(base.val)


ins = child()
ins.f()

ins2 = child2()
ins2.f()

# child, child2各自继承自base, 相当于复制， child对base做的修改对所有继承类生效