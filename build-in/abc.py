
x = 'abc'


def foo():
    global x
    print(x)

if __name__ == "__main__":
    x = 'mmm'
    foo()

