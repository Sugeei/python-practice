class Number:
    def __iter__(self):
        self.a=1
        return self

    def __next__(self):
        x=self.a
        self.a+=1
        return x

myclass = Number()
myiter = iter(myclass)

print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))

for n in myiter:
    print(n)
    import time
    time.sleep(1)