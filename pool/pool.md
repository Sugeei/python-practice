apply_async 将所有任务先放到等待队列，如果任务量过大，可能撑爆内存，可以用len(pool._cache)判断是否大于当前进程数。大于则等待

如果传给pool的class实例的参数中有一个100M的dict, 查看它们的Id会发现所有地址都一样， 也就是说没有copy,用的是同一个地址的变量，
但是查看占用内存会发现所有实例的大小都是100多M

timeout
https://stackoverflow.com/questions/29494001/how-can-i-abort-a-task-in-a-multiprocessing-pool-after-a-timeout

https://www.programcreek.com/python/example/29809/multiprocessing.TimeoutError

对pool, terminate, close的解释比较清楚
http://blog.csdn.net/fireroll/article/details/46515115

a method to abort a task in a multiprocessing.pool after a timeout
- a pretty good example, pool_track.py
https://stackoverflow.com/questions/29494001/how-can-i-abort-a-task-in-a-multiprocessing-pool-after-a-timeout

# what does pool_track do:
- when get a task from queue, consumer will call pool.apply_async to start a process to run abortable_worker.
- in function abortable_worker, it will do the timeout management. That is when time out, it will raise an exception to terminate the process
- this is an example of combining pool, queue, and timeout management

threading.condition
http://beginman.cn/python/2015/11/30/python-threading-condition/
列表并不是一开始就有的；而是通过线程”create”创建的。如果”set”或者”print” 在”create”还没有运行的时候就访问列表，将会出现一个异常。

Interrupt the Python multiprocessing.Pool in graceful way
http://xcodest.me/interrupt-the-python-multiprocessing-pool-in-graceful-way.html
- pool_with_interrupt.py

How ctrl+c works
https://unix.stackexchange.com/questions/149741/why-is-sigint-not-propagated-to-child-process-when-sent-to-its-parent-process/149756#149756

How to kill thread in python when timeout happens
https://eli.thegreenplace.net/2011/08/22/how-not-to-set-a-timeout-on-a-computation-in-python



The way Multiprocessing works in Python is such that each child process imports the parent script. In Python, when you import a script, everything not defined within a function is executed. As I understand it, __name__ is changed on an import of the script (Check this SO answer here for a better understanding), which is different than if you ran the script on the command line directly, which would result in __name__ == '__main__'. This import results in __name__ not equalling '__main__', which is why the code in if __name__ == '__main__': is not executed for your subprocess.

Anything you don't want executed during subprocess calls should be moved into your if __name__ == '__main__': section of your code, as this will only run for the parent process, i.e. the script you run initially.



Here's a short example of calling an object's method with arguments with a pool.

The first problem is that only function defined at the top level of a module can be pickled.
Unix-based systems have a way of getting around this limitation, but this shouldn't be relied upon.
So you must define a function that takes the object you want and arguments needed to call the relevant method.
https://stackoverflow.com/questions/29816361/python-multiprocessing-pool-ignores-class-method
for method in a class , need to do this to get pool working:
```
# new an instance fisrtly
operator = Operator(ticker, datelist, init_data, defaultdict(list))
# then pass the instance as parameter
res = p.apply_async(run, args=(operator,))
```

# TODO
https://stackoverflow.com/questions/42584525/python-multiprocessing-debugging-oserror-errno-12-cannot-allocate-memory