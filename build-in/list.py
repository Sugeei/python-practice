# coding=utf-8

# 默认的list只在函数定义的时候被创建一次。
# 之后不指定list参数调用extendList函数时，
# 使用的都是同一个list。
# 这是因为带默认参数的表达式是在函数定义的时候被计算的，而不是在函数调用时。


def extendList(val, list=[]):
    list.append(val)
    return list


list1 = extendList(10)
list2 = extendList(123, [])
list3 = extendList('a')

print("list1 = %s" % list1)
print("list2 = %s" % list2)
print("list3 = %s" % list3)

# list = [ [ ] ] * 5创建了一个元素是5个列表的列表。
# 但是，这里要理解的关键是，list = [ [ ] ] * 5并没有创建一个包含5个不同列表的列表。
# 创建的这个列表里的5个列表，是对同一个列表的引用（a a list of 5 references to the same list）
list = [[]] * 5
print(list)
list[0].append(10)
print(list)
list[1].append(20)
print(list)
list.append(30)
print(list)
