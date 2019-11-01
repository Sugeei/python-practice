
# # https://stackoverflow.com/questions/41379464/python-apply-async-does-not-call-method
import multiprocessing as mp
import random, time


def check(arg):
    process = mp.current_process
    if not hasattr(process, "main_class"):
        process.main_class = MainClass()
    process.main_class.check(arg)


class MainClass:
    def __init__(self):
        self.value = random.randrange(100)

    def check(self, arg):
        time.sleep(random.uniform(0.01, 0.3))
        print(id(self), self.value, arg)


def main():
    # mc = MainClass()

    with mp.Pool(processes=2) as pool:
        temp = [pool.apply_async(check, (i,)) for i in range(8)]
        results = [t.get() for t in temp]


# 在 Windows 上，子进程会自动 import 启动它的这个文件，而在 import 的时候是会执行这些语句的。
# 如果你这么写的话就会无限递归创建子进程报错。
# 所以必须把创建子进程的部分用那个 if 判断保护起来，import 的时候 __name__ 不是 __main__ ，就不会递归运行了。
if __name__ == "__main__":
    main()
