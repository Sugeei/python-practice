import importlib
import importlib.util
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