# python process how to wait them to finish

# https://docs.python.org/2/library/multiprocessing.html#multiprocessing.Process.join

#
# join([timeout])
#
#     Block the calling thread until the process whose join() method is called terminates or until the optional timeout occurs.
#
#     If timeout is None then there is no timeout.
#
#     A process can be joined many times.
#
#     A process cannot join itself because this would cause a deadlock. It is an error to attempt to join a process before it has been started.
#
#
