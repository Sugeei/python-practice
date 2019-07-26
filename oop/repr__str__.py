class Car:
    def __init__(self):
        # self.color = color
        # self.mileage = mileage
        pass

    def __repr__(self):
        return '__repr__ for Car'

    def __str__(self):
        return '__str__ for Car'

print(str(Car()))
print(repr(Car()))