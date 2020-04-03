https://rushter.com/blog/python-memory-managment/
https://rushter.com/blog/python-garbage-collector/

https://stackoverflow.com/questions/42584525/python-multiprocessing-debugging-oserror-errno-12-cannot-allocate-memory
Python multiprocessing - Debugging OSError: [Errno 12] Cannot allocate memory

```
When using a multiprocessing.Pool, the default way to start the processes is fork. The issue with fork is that the entire process is duplicated. (see details here). Thus if your main process is already using a lot of memory, this memory will be duplicated, reaching this MemoryError. For instance, if your main process use 2GB of memory and you use 8 subprocesses, you will need 18GB in RAM.

You should try using a different start method such as 'forkserver' or 'spawn':

from multiprocessing import set_start_method, Pool
set_start_method('forkserver')

# You can then start your Pool without each process
# cloning your entire memory
pool = Pool()
func = partial(parallelUpdateJSON, paramMatch, predictionmatrix)
pool.map(func, data)

These methods avoid duplicating the workspace of your Process but can be a bit slower to start as you need to reload the modules you are using.

```

https://stackoverflow.com/questions/14124588/shared-memory-in-multiprocessing


Generally speaking, there are two ways to share the same data:

    Multithreading
    Shared memory

Python's multithreading is not suitable for CPU-bound tasks (because of the GIL), so the usual solution in that case is to go on multiprocessing. However, with this solution you need to explicitly share the data, using multiprocessing.Value and multiprocessing.Array.

Note that usually sharing data between processes may not be the best choice, because of all the synchronization issues; an approach involving actors exchanging messages is usually seen as a better choice. See also Python documentation:

    As mentioned above, when doing concurrent programming it is usually best to avoid using shared state as far as possible. This is particularly true when using multiple processes.

    However, if you really do need to use some shared data then multiprocessing provides a couple of ways of doing so.

In your case, you need to wrap l1, l2 and l3 in some way understandable by multiprocessing (e.g. by using a multiprocessing.Array), and then pass them as parameters.
Note also that, as you said you do not need write access, then you should pass lock=False while creating the objects, or all access will be still serialized.
shareedit
edited Jan 4 '13 at 7:48

https://stackoverflow.com/questions/10721915/shared-memory-objects-in-multiprocessing
If you use an operating system that uses copy-on-write fork() semantics (like any common unix), then as long as you never alter your data structure it will be available to all child processes without taking up additional memory. You will not have to do anything special (except make absolutely sure you don't alter the object).


