from selenium import webdriver
import selenium
from config.base import phantomjs
from random import randint
import time
from src.proxies import proxymanage


class AccessBase():
    def __init__(self):
        self.max_wait = 60
        self.max_tried = 3

    # def
    def access(self, url, driver):

        # driver = webdriver.PhantomJS(executable_path=phantomjs, service_args=service_args)
        driver.set_window_size(1024, 768)
        driver.set_page_load_timeout(self.max_wait)
        driver.set_script_timeout(self.max_wait)

        try:
            driver.get(url)
        except selenium.common.exceptions.TimeoutException as timeout:
            pass
            # time.
        # time.sleep(randint(2, 8))
        title = driver.title
        page = driver.page_source
        return title, page

    def get(self, url, maxtry=1):
        driver = webdriver.PhantomJS(executable_path=phantomjs)
        return self.access(url, driver)

    def get_with_proxy(self, url):
        title = ''
        tried = 0
        while title == '' and tried < self.max_tried:
            proxy = proxymanage.get_proxy()
            # PROXY = "23.23.23.23:3128"  # IP:PORT or HOST:PORT
            service_args = [
                '--proxy=%s' % proxy,
                '--proxy-type=http',
            ]
            driver = webdriver.PhantomJS(executable_path=phantomjs, service_args=service_args)
            title, page = self.access(url, driver)
            if len(title) == 0:
                proxymanage.remove_proxy(proxy)

            tried += 1
            print('get with proxy tried counts=%s' % tried)

        return title, page

    def get_with_try(self, url, maxtry=1, searchflag=''):
        driver = webdriver.PhantomJS(executable_path=phantomjs)
        driver.get(url)
        time.sleep(randint(2, 5))
        # title = driver.title
        page = driver.page_source
        tried = 0
        target = ''
        while len(target) == 0 and tried < maxtry:
            time.sleep(3)
            target = page.find(searchflag)

        title = driver.title
        page = driver.page_source
        return title, page


accessbase = AccessBase()

if __name__ == "__main__":
    url = "https://www.landchina.com/default.aspx?tabid=386&comname=default&wmguid=75c72564-ffd9-426a-954b-8ac2df0903b7&recorderguid=9A59E61025A951EDE055000000000001"
    url = "https://www.landchina.com/default.aspx?tabid=386&comname=default&wmguid=75c72564-ffd9-426a-954b-8ac2df0903b7&recorderguid=d226523a-88df-4c1e-b183-a004b8a560b1"
    url = 'https://www.landchina.com/default.aspx?tabid=263&ComName=default'
    title, page = accessbase.get(url)
    title, page = accessbase.get_with_proxy(url)
    pass
