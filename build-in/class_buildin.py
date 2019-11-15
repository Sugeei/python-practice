# BaseAccess().__class__
# BaseAccess().__dir__()
# BaseAccess.__dict__

class Cdemo():
    def __init__(self):
        pass

    def funca(self):
        print(Cdemo.__dict__)

    def funcm(self):
        print(Cdemo.__class__)

    def funcx(self):
        print(Cdemo.__dir__())

    def __call__(self, *args, **kwargs):
        print("call")


c = Cdemo()
print('-' * 20)
print(c())
print('-' * 20)
print(Cdemo().__dir__())
print(Cdemo.__dict__)

# set step
l = list(range(10))
print(l[::2])
print(l[::3])

# class __call__
# https: // www.jianshu.com / p / e1d95c4e1697

# https://docs.python.org/3/library/concurrent.futures.html
