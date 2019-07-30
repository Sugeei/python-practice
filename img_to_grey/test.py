def f(para):
    para=3

def f2(*arg):
    arg.append(2)
b=[1]
f(b)
print (b)

f2(*b)
print(b)