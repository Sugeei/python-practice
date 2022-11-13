import importlib
import importlib.util
import os
import sys
foo = importlib.import_module('darec')
print(foo)
import inspect
# m = foo.DAREC()
modulespc = importlib.util.spec_from_file_location('darec', 'darec.py')
module = importlib.util.module_from_spec(modulespc)

modulespc.loader.exec_module(module)
# sys.modules['darec'] = module

print(module)
print(module.__name__)
m = module.__name__
# m()
# m = module
# import darec
# m =
for name, clazz in inspect.getmembers(module):
    if inspect.isclass(clazz):
        obj=clazz()
        obj.run()

import importlib.util
path = os.path.dirname(__file__)


spec = importlib.util.spec_from_file_location("dynamicimp", path)

foo = importlib.util.module_from_spec(spec)

spec.loader.exec_module(foo)

print(foo.tmp)

class tmp:
    def __init__(self, init):
        self.init = init
    def run(self, param):
        return self.init+param
path = os.path.dirname(__file__)
print(path)
module = importlib.import_module(path)
obj = getattr(module, 'tmp')

obj(1).run(2)