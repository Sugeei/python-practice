python3, import
relative import
https://stackoverflow.com/questions/12172791/changes-in-import-statement-python3
```
Python 3 no longer supports that since it's not explicit whether you want the 'relative' or 'absolute' base. In other words, if there was a Python package named base installed in the system, you'd get the wrong one.

Instead it requires you to use explicit imports which explicitly specify location of a module on a path-alike basis. Your derived.py would look like:

from .base import BaseThing
```
https://docs.python.org/3/reference/import.html