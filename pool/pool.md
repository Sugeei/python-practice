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