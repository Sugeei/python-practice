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


