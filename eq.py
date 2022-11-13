class BrokenComparison:
    def __eq__(self, other):
        return True


# https://realpython.com/null-in-python/#understanding-null-in-python

b = BrokenComparison()

b == True

class BrokenComparison:
    def __eq__(self, other):
        return "YES"
