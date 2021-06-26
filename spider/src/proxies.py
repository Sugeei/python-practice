from random import randint
#
# PROXIES = [
#     "122.245.67.174:808",
#     "221.216.94.77:808",
#     "115.230.13.202:808",
#     "183.78.183.156:82",
#     "121.31.100.121:8123",
#     "119.5.1.53:808",
#     "61.232.254.39:3128"
#
# ]

import os

dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

with open(os.path.join(dir, 'proxy', 'ip.txt'), 'r') as fh:
    ps = fh.readlines()
ps = [x.strip() for x in ps]


class ProxyManage():
    def __init__(self):
        self.proxies = ps

    def get_proxy(self):
        idx = randint(0, len(self.proxies) - 1)
        proxy = self.proxies[idx]
        return proxy

    def remove_proxy(self, proxy):
        # to remove proxy cannot get valid response
        self.proxies.pop(self.proxies.index(proxy))
        print("removed_proxy %s " % proxy)


proxymanage = ProxyManage()
if __name__ == "__main__":
    ps = ['1', '2', '30']
    p = ProxyManage()
    p.remove_proxy('2')
    print(p.proxies)
