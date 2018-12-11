# coding=utf-8

# Say I have a list
fruits = ["apple", "orange", "banana", "lemon"]
# I try to figure out whether a given character like "p" exists in one of these elements
if any("p" in element for element in fruits):
    print "yes"
else:
    print "failed"

# If I want to know whether "a" can be found in all these elements
if all("p" in element for element in fruits):
    print "yes"
else:
    print "failed"


print any([])