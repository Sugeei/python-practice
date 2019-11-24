import time
import threading
import signal
from common.logger import flow_log


class Job(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        # The shutdown_flag is a threading.Event object that
        # indicates whether the thread should be terminated.
        self.shutdown_flag = threading.Event()

        # ... Other thread setup code here ...

    def run(self):
        flow_log.info('Thread #%s started' % self.ident)

        while not self.shutdown_flag.is_set():
            # ... Job code here ...
            time.sleep(0.5)

        # ... Clean shutdown code here ...
        flow_log.info('Thread #%s stopped' % self.ident)


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


def service_shutdown(signum, frame):
    flow_log.info('Caught signal %d' % signum)
    raise ServiceExit


def main():
    # Register the signal handlers
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)

    flow_log.info('Starting main program')

    # Start the job threads
    try:
        j1 = Job()
        j2 = Job()
        j1.start()
        j2.start()

        # Keep the main thread running, otherwise signals are ignored.
        while True:
            time.sleep(0.5)

    except ServiceExit:
        # Terminate the running threads.
        # Set the shutdown flag on each thread to trigger a clean shutdown of each thread.
        j1.shutdown_flag.set()
        j2.shutdown_flag.set()
        # Wait for the threads to close...
        j1.join()
        j2.join()

    flow_log.info('Exiting main program')


if __name__ == '__main__':
    main()
