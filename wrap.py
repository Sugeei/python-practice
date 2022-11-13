def my_decorator(original_func):
    def wrapper(*args, **kwargs):
        """this is wrapper documentation...."""
        original_func(*args, **kwargs)

    return wrapper


def greet_hindi(name: str):
    """Greets in english"""
    print('Namaste, {name}!', name)

@my_decorator
def greet_french(name: str):
    """Greets in french"""
    print('Bonjour, {name}!', name)

greet_hindi('Philip')
greet_french('Rohan')

print(greet_hindi.__name__,greet_hindi.__doc__)
print(greet_french.__name__,greet_french.__doc__)

"""If you look at the image above; names and documentations of functions greet_hindi and greet_french aren’t printed.
Instead, the name and documentation of the wrapper function of my_decorator got printed.

What is causing it? If you take a glance at my_decorator; it returns the wrapper function, which is responsible for this.
With this in mind, decorators do not preserve the information or details of the functions(first-order functions)
passed into them as arguments. Therefore, this problem needs to be dealt with.

"""

"""A straightforward solution is to use the functools.wraps().
Hence, use it to decorate the wrapper function of the decorator.
In other words, we need to put it above the wrapper function.
The ‘@’ symbol, like shown below, and the first-class function passed as an argument.

"""
import functools
def my_decorator2(original_func):
    @functools.wraps(original_func)
    def wrapper(*args, **kwargs):
        """this is wrapper documentation...."""
        original_func(*args,**kwargs)
    return wrapper


@my_decorator2
def greet_french2(name: str):
    """Greets in french"""
    print('Bonjour, {name}!', name)

print(greet_hindi.__name__,greet_hindi.__doc__)
print(greet_french2.__name__,greet_french2.__doc__)
