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