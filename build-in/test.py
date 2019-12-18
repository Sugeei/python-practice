import os

with open(str(os.__file__), "r") as f:
    print(f.read())