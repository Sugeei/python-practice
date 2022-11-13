from pak.abc import foo

foo()

if __name__ == "__main__":
    global x
    x = 'xyz'
    foo()
    print(x)