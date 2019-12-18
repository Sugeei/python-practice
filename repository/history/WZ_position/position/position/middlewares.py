# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class PositionSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

import random
import base64
from .settings import PROXIES


class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)
        if proxy['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            encoded_user_pass = proxy['user_pass'] #base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
	        # print("**************ProxyMiddleware have pass************" + proxy['ip_port'])
        else:
	        # print("**************ProxyMiddleware no pass************" + proxy['ip_port'])
            request.meta['proxy'] = "http://%s" % proxy['ip_port']


from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class RandomUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        if ua:
            #显示当前使用的useragent
            print ("********Current UserAgent:%s************" %ua)

            #记录
            # log.msg('Current UserAgent: '+ua, level='INFO')
            request.headers.setdefault('User-Agent', ua)

    #the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    #for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
    user_agent_list = [\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
       ]


# #!/usr/bin/python
# # -*- coding: utf-8 -*-
# import os
# import logging
# from datetime import datetime, timedelta
# from twisted.web._newclient import ResponseNeverReceived
# from twisted.internet.error import TimeoutError, ConnectionRefusedError, ConnectError
# # import fetch_free_proxy
#
# logger = logging.getLogger(__name__)
#
# class HttpProxyMiddleware(object):
#     # 遇到这些类型的错误直接当做代理不可用处理掉, 不再传给retrymiddleware
#     DONT_RETRY_ERRORS = (TimeoutError, ConnectionRefusedError, ResponseNeverReceived, ConnectError, ValueError)
#
#     def __init__(self, settings):
#         # 保存上次不用代理直接连接的时间点
#         self.last_no_proxy_time = datetime.now()
#         # 一定分钟数后切换回不用代理, 因为用代理影响到速度
#         self.recover_interval = 20
#         # 一个proxy如果没用到这个数字就被发现老是超时, 则永久移除该proxy. 设为0则不会修改代理文件.
#         self.dump_count_threshold = 20
#         # 存放代理列表的文件, 每行一个代理, 格式为ip:port, 注意没有http://, 而且这个文件会被修改, 注意备份
#         self.proxy_file = "proxyes.dat"
#         # 是否在超时的情况下禁用代理
#         self.invalid_proxy_flag = True
#         # 当有效代理小于这个数时(包括直连), 从网上抓取新的代理, 可以将这个数设为为了满足每个ip被要求输入验证码后得到足够休息时间所需要的代理数
#         # 例如爬虫在十个可用代理之间切换时, 每个ip经过数分钟才再一次轮到自己, 这样就能get一些请求而不用输入验证码.
#         # 如果这个数过小, 例如两个, 爬虫用A ip爬了没几个就被ban, 换了一个又爬了没几次就被ban, 这样整个爬虫就会处于一种忙等待的状态, 影响效率
#         self.extend_proxy_threshold = 10
#         # 初始化代理列表
#         self.proxyes = [{"proxy": None, "valid": True, "count": 0}]
#         # 初始时使用0号代理(即无代理)
#         self.proxy_index = 0
#         # 表示可信代理的数量(如自己搭建的HTTP代理)+1(不用代理直接连接)
#         self.fixed_proxy = len(self.proxyes)
#         # 上一次抓新代理的时间
#         self.last_fetch_proxy_time = datetime.now()
#         # 每隔固定时间强制抓取新代理(min)
#         self.fetch_proxy_interval = 120
#         # 一个将被设为invalid的代理如果已经成功爬取大于这个参数的页面， 将不会被invalid
#         self.invalid_proxy_threshold = 200
#         # 从文件读取初始代理
# 	if os.path.exists(self.proxy_file):
# 	    with open(self.proxy_file, "r") as fd:
# 		lines = fd.readlines()
# 		for line in lines:
# 		    line = line.strip()
# 		    if not line or self.url_in_proxyes("http://" + line):
# 			continue
# 		    self.proxyes.append({"proxy": "http://"  + line,
# 					"valid": True,
# 					"count": 0})
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(crawler.settings)
#
#     def url_in_proxyes(self, url):
#         """
#         返回一个代理url是否在代理列表中
#         """
#         for p in self.proxyes:
#             if url == p["proxy"]:
#                 return True
#         return False
#
#     def reset_proxyes(self):
#         """
#         将所有count>=指定阈值的代理重置为valid,
#         """
#         logger.info("reset proxyes to valid")
#         for p in self.proxyes:
#             if p["count"] >= self.dump_count_threshold:
#                 p["valid"] = True
#
#     def fetch_new_proxyes(self):
#         """
#         从网上抓取新的代理添加到代理列表中
#         """
#         logger.info("extending proxyes using fetch_free_proxyes.py")
#         new_proxyes = fetch_free_proxyes.fetch_all()
#         logger.info("new proxyes: %s" % new_proxyes)
#         self.last_fetch_proxy_time = datetime.now()
#
#         for np in new_proxyes:
#             if self.url_in_proxyes("http://" + np):
#                 continue
#             else:
#                 self.proxyes.append({"proxy": "http://"  + np,
#                                      "valid": True,
#                                      "count": 0})
#         if self.len_valid_proxy() < self.extend_proxy_threshold: # 如果发现抓不到什么新的代理了, 缩小threshold以避免白费功夫
#             self.extend_proxy_threshold -= 1
#
#     def len_valid_proxy(self):
#         """
#         返回proxy列表中有效的代理数量
#         """
#         count = 0
#         for p in self.proxyes:
#             if p["valid"]:
#                 count += 1
#         return count
#
#     def inc_proxy_index(self):
#         """
#         将代理列表的索引移到下一个有效代理的位置
#         如果发现代理列表只有fixed_proxy项有效, 重置代理列表
#         如果还发现已经距离上次抓代理过了指定时间, 则抓取新的代理
#         """
#         assert self.proxyes[0]["valid"]
#         while True:
#             self.proxy_index = (self.proxy_index + 1) % len(self.proxyes)
#             if self.proxyes[self.proxy_index]["valid"]:
#                 break
#
#         # 两轮proxy_index==0的时间间隔过短， 说明出现了验证码抖动，扩展代理列表
#         if self.proxy_index == 0 and datetime.now() < self.last_no_proxy_time + timedelta(minutes=2):
#             logger.info("captcha thrashing")
#             self.fetch_new_proxyes()
#
#         if self.len_valid_proxy() <= self.fixed_proxy or self.len_valid_proxy() < self.extend_proxy_threshold: # 如果代理列表中有效的代理不足的话重置为valid
#             self.reset_proxyes()
#
#         if self.len_valid_proxy() < self.extend_proxy_threshold: # 代理数量仍然不足, 抓取新的代理
#             logger.info("valid proxy < threshold: %d/%d" % (self.len_valid_proxy(), self.extend_proxy_threshold))
#             self.fetch_new_proxyes()
#
#         logger.info("now using new proxy: %s" % self.proxyes[self.proxy_index]["proxy"])
#
#         # 一定时间没更新后可能出现了在目前的代理不断循环不断验证码错误的情况, 强制抓取新代理
#         #if datetime.now() > self.last_fetch_proxy_time + timedelta(minutes=self.fetch_proxy_interval):
#         #    logger.info("%d munites since last fetch" % self.fetch_proxy_interval)
#         #    self.fetch_new_proxyes()
#
#     def set_proxy(self, request):
#         """
#         将request设置使用为当前的或下一个有效代理
#         """
#         proxy = self.proxyes[self.proxy_index]
#         if not proxy["valid"]:
#             self.inc_proxy_index()
#             proxy = self.proxyes[self.proxy_index]
#
#         if self.proxy_index == 0: # 每次不用代理直接下载时更新self.last_no_proxy_time
#             self.last_no_proxy_time = datetime.now()
#
#         if proxy["proxy"]:
#             request.meta["proxy"] = proxy["proxy"]
#         elif "proxy" in request.meta.keys():
#             del request.meta["proxy"]
#         request.meta["proxy_index"] = self.proxy_index
#         proxy["count"] += 1
#
#     def invalid_proxy(self, index):
#         """
#         将index指向的proxy设置为invalid,
#         并调整当前proxy_index到下一个有效代理的位置
#         """
#         if index < self.fixed_proxy: # 可信代理永远不会设为invalid
# 	    self.inc_proxy_index()
#             return
#
#         if self.proxyes[index]["valid"]:
#             logger.info("invalidate %s" % self.proxyes[index])
#             self.proxyes[index]["valid"] = False
#             if index == self.proxy_index:
#                 self.inc_proxy_index()
#
#             if self.proxyes[index]["count"] < self.dump_count_threshold:
#                 self.dump_valid_proxy()
#
#     def dump_valid_proxy(self):
#         """
#         保存代理列表中有效的代理到文件
#         """
#         if self.dump_count_threshold <= 0:
#             return
#         logger.info("dumping proxyes to file")
#         with open(self.proxy_file, "w") as fd:
#             for i in range(self.fixed_proxy, len(self.proxyes)):
#                 p = self.proxyes[i]
#                 if p["valid"] or p["count"] >= self.dump_count_threshold:
#                     fd.write(p["proxy"][7:]+"\n") # 只保存有效的代理
#
#     def process_request(self, request, spider):
#         """
#         将request设置为使用代理
#         """
#         if self.proxy_index > 0  and datetime.now() > (self.last_no_proxy_time + timedelta(minutes=self.recover_interval)):
#             logger.info("After %d minutes later, recover from using proxy" % self.recover_interval)
#             self.last_no_proxy_time = datetime.now()
#             self.proxy_index = 0
#         request.meta["dont_redirect"] = True  # 有些代理会把请求重定向到一个莫名其妙的地址
#
#         # spider发现parse error, 要求更换代理
#         if "change_proxy" in request.meta.keys() and request.meta["change_proxy"]:
#             logger.info("change proxy request get by spider: %s"  % request)
#             self.invalid_proxy(request.meta["proxy_index"])
#             request.meta["change_proxy"] = False
#         self.set_proxy(request)
#
#     def process_response(self, request, response, spider):
#         """
#         检查response.status, 根据status是否在允许的状态码中决定是否切换到下一个proxy, 或者禁用proxy
#         """
#         if "proxy" in request.meta.keys():
#             logger.debug("%s %s %s" % (request.meta["proxy"], response.status, request.url))
#         else:
#             logger.debug("None %s %s" % (response.status, request.url))
#
#         # status不是正常的200而且不在spider声明的正常爬取过程中可能出现的
#         # status列表中, 则认为代理无效, 切换代理
#         if response.status != 200 \
#                 and (not hasattr(spider, "website_possible_httpstatus_list") \
#                              or response.status not in spider.website_possible_httpstatus_list):
#             logger.info("response status not in spider.website_possible_httpstatus_list")
#             self.invalid_proxy(request.meta["proxy_index"])
#             new_request = request.copy()
#             new_request.dont_filter = True
#             return new_request
#         else:
#             return response
#
#     def process_exception(self, request, exception, spider):
#         """
#         处理由于使用代理导致的连接异常
#         """
#         logger.debug("%s exception: %s" % (self.proxyes[request.meta["proxy_index"]]["proxy"], exception))
#         request_proxy_index = request.meta["proxy_index"]
#
#         # 只有当proxy_index>fixed_proxy-1时才进行比较, 这样能保证至少本地直连是存在的.
#         if isinstance(exception, self.DONT_RETRY_ERRORS):
#             if request_proxy_index > self.fixed_proxy - 1 and self.invalid_proxy_flag: # WARNING 直连时超时的话换个代理还是重试? 这是策略问题
#                 if self.proxyes[request_proxy_index]["count"] < self.invalid_proxy_threshold:
#                     self.invalid_proxy(request_proxy_index)
#                 elif request_proxy_index == self.proxy_index:  # 虽然超时，但是如果之前一直很好用，也不设为invalid
#                     self.inc_proxy_index()
#             else:               # 简单的切换而不禁用
#                 if request.meta["proxy_index"] == self.proxy_index:
#                     self.inc_proxy_index()
#             new_request = request.copy()
#             new_request.dont_filter = True
#             return new_request