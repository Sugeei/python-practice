python3, import
to read
https://docs.python.org/3/reference/import.html

https://docs.python.org/3/reference/import.html

https://alex.dzyoba.com/blog/python-import/
Module search path is a list of directories (available at runtime as sys.path) that interpreter uses to locate modules. It is initialized with the path to Python standard modules (/usr/lib64/python3.6), site-packages where pip puts everything you install globally, and also a directory that depends on how you run a module. If you run a module as a file like python3 pizzashop/shop.py the path to containing directory (pizzashop) is added to sys.path. Otherwise, including running with -m option, the current directory (as in pwd) is added to module search path. We can check it by printing sys.path in pizzashop/shop.py:

$ pwd
/home/avd/dev/python-imports

$ tree
.
├── pizzapy
│   ├── __init__.py
│   ├── __main__.py
│   ├── menu.py
│   └── pizza.py
└── pizzashop
    ├── __init__.py
    └── shop.py

$ python3 pizzashop/shop.py
['/home/avd/dev/python-imports/pizzashop',
 '/usr/lib64/python36.zip',
 '/usr/lib64/python3.6',
 '/usr/lib64/python3.6/lib-dynload',
 '/usr/local/lib64/python3.6/site-packages',
 '/usr/local/lib/python3.6/site-packages',
 '/usr/lib64/python3.6/site-packages',
 '/usr/lib/python3.6/site-packages']
Traceback (most recent call last):
  File "pizzashop/shop.py", line 5, in <module>
    import pizzapy.menu
ModuleNotFoundError: No module named 'pizzapy'

$ python3 -m pizzashop.shop
['',
 '/usr/lib64/python36.zip',
 '/usr/lib64/python3.6',
 '/usr/lib64/python3.6/lib-dynload',
 '/usr/local/lib64/python3.6/site-packages',
 '/usr/local/lib/python3.6/site-packages',
 '/usr/lib64/python3.6/site-packages',
 '/usr/lib/python3.6/site-packages']
pizza.py module name is pizza
[<pizza.Pizza object at 0x7f2f75747f28>, <pizza.Pizza object at 0x7f2f75747f60>, <pizza.Pizza object at 0x7f2f75747fd0>]

As you can see in the first case we have the pizzashop dir in our path and so we cannot find sibling pizzapy package, while in the second case the current dir (denoted as '') is in sys.path and it contains both packages.

    Python has module search path available at runtime as sys.path
    If you run a module as a script file, the containing directory is added to sys.path, otherwise, the current directory is added to it

This problem of importing the sibling package often arise when people put a bunch of test or example scripts in a directory or package next to the main package. Here is a couple of StackOverflow questions:

    https://stackoverflow.com/q/6323860
    https://stackoverflow.com/q/6670275

The good solution is to avoid the problem – put tests or examples in the package itself and use relative import. The dirty solution is to modify sys.path at runtime (yay, dynamic!) by adding the parent directory of the needed package. People actually do this despite it’s an awful hack.
