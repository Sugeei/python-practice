import abc


# https://www.cnblogs.com/weihengblog/p/8528967.html
class Demo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self):
        pass


demo = Demo() # this class can't be instantiated
