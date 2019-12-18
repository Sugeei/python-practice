#!/usr/bin/python
# -*- coding: utf-8 -*-
# import urllib2
import logging

logger = logging.getLogger(__name__)

# def get_html(url):
    # request = urllib2.Request(url)
    # request.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36")
    # html = urllib2.urlopen(request)
    # return html.read()

from proxy_verify import Proxy, Spider
from client_config import CLIENT_CONFIG


from bs4 import BeautifulSoup
def get_soup(response):
    return BeautifulSoup(response.body, "lxml")
    # return soup
    # proxy = Proxy(url=url, headers=CLIENT_CONFIG['headers'])
    # ips_list = yield proxy.test_proxy()

def fetch_kxdaili(page):
    """
    从www.kxdaili.com抓取免费代理
    """
    proxyes = []
    try:
        url = "http://www.kxdaili.com/dailiip/1/%d.html" % page
        proxy = Proxy(url=url, headers=CLIENT_CONFIG['headers'])
        proxyes = yield proxy.fetch_kxdaili()
    except:
        logger.warning("fail to fetch from kxdaili")
    return proxyes

def img2port(img_url):
    """
    mimvp.com的端口号用图片来显示, 本函数将图片url转为端口, 目前的临时性方法并不准确
    """
    code = img_url.split("=")[-1]
    if code.find("AO0OO0O")>0:
        return 80
    else:
        return None

def fetch_mimvp():
    """
    从http://proxy.mimvp.com/free.php抓免费代理
    """
    proxyes = []
    try:
        url = "http://proxy.mimvp.com/free.php?proxy=in_hp"
        soup = get_soup(url)
        table = soup.find("div", attrs={"id": "list"}).table
        tds = table.tbody.find_all("td")
        for i in range(0, len(tds), 10):
            id = tds[i].text
            ip = tds[i+1].text
            port = img2port(tds[i+2].img["src"])
            response_time = tds[i+7]["title"][:-1]
            transport_time = tds[i+8]["title"][:-1]
            if port is not None and float(response_time) < 1 :
                proxy = "%s:%s" % (ip, port)
                proxyes.append(proxy)
    except:
        logger.warning("fail to fetch from mimvp")
    return proxyes

def fetch_xici():
    """
    http://www.xicidaili.com/nn/
    """
    proxyes = []
    try:
        url = "http://www.xicidaili.com/nn/"
        proxy = Proxy(url=url, headers=CLIENT_CONFIG['headers'])
        proxyes = proxy.fetch_xici()
    except:
        logger.warning("fail to fetch from xici")
    return proxyes

def fetch_ip181():
    """
    http://www.ip181.com/
    """
    proxyes = []
    try:
        url = "http://www.ip181.com/"
        soup = get_soup(url)
        table = soup.find("table")
        trs = table.find_all("tr")
        for i in range(1, len(trs)):
            tds = trs[i].find_all("td")
            ip = tds[0].text
            port = tds[1].text
            latency = tds[4].text[:-2]
            if float(latency) < 1:
                proxyes.append("%s:%s" % (ip, port))
    except Exception as e:
        logger.warning("fail to fetch from ip181: %s" % e)
    return proxyes

def fetch_httpdaili():
    """
    http://www.httpdaili.com/mfdl/
    更新比较频繁
    """
    proxyes = []
    try:
        url = "http://www.httpdaili.com/mfdl/"
        soup = get_soup(url)
        table = soup.find("div", attrs={"kb-item-wrap11"}).table
        trs = table.find_all("tr")
        for i in range(1, len(trs)):
            try:
                tds = trs[i].find_all("td")
                ip = tds[0].text
                port = tds[1].text
                type = tds[2].text
                if type == u"匿名":
                    proxyes.append("%s:%s" % (ip, port))
            except:
                pass
    except Exception as e:
        logger.warning("fail to fetch from httpdaili: %s" % e)
    return proxyes

def fetch_66ip():
    """    
    http://www.66ip.cn/
    每次打开此链接都能得到一批代理, 速度不保证
    """
    proxyes = []
    try:
        # 修改getnum大小可以一次获取不同数量的代理
        url = "http://www.66ip.cn/nmtq.php?getnum=10&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=1&proxytype=0&api=66ip"
        content = get_html(url)
        urls = content.split("</script>")[-1].split("<br />")
        for u in urls:
            if u.strip():
                proxyes.append(u.strip())
    except Exception as e:
        logger.warning("fail to fetch from httpdaili: %s" % e)
    return proxyes


def check(proxy):
    import urllib
    url = "http://www.baidu.com/js/bdsug.js?v=1.0.3.0"
    # proxy_handler = urllib2.ProxyHandler({'http': "http://" + proxy})
    # opener = urllib2.build_opener(proxy_handler,urllib2.HTTPHandler)
    # try:
    #     response = opener.open(url,timeout=3)
    #     return response.code == 200
    # except Exception:
    #     return False

def verifyproxy(proxy):
    pass

def fetch_all(endpage=2):
    # proxy = Proxy(url=url, headers=CLIENT_CONFIG['headers'])

    proxyes = []
    proxyes += fetch_xici()
    for i in range(1, endpage):
        proxyes += fetch_kxdaili(i)
    # proxyes += fetch_mimvp()
    proxyes += fetch_ip181()
    proxyes += fetch_httpdaili()
    proxyes += fetch_66ip()
    valid_proxyes = []
    logger.info("checking proxyes validation")
    for p in proxyes:
        if check(p):
            valid_proxyes.append(p)
    return valid_proxyes

if __name__ == '__main__':
    import sys
    root_logger = logging.getLogger("")
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(name)-8s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    proxyes = fetch_all()
    #print check("202.29.238.242:3128")
    for p in proxyes:
        # print p
        pass
