from selenium import webdriver
from config.base import phantomjs
from random import randint
import time


class AccessBase():
    def get(self, url, maxtry=1):
        driver = webdriver.PhantomJS(executable_path=phantomjs)
        driver.get(url)
        time.sleep(randint(2, 8))
        title = driver.title
        page = driver.page_source
        return title, page

    def get_with_try(self, url, maxtry=1, searchflag=''):
        driver = webdriver.PhantomJS(executable_path=phantomjs)
        driver.get(url)
        time.sleep(randint(2, 5))
        # title = driver.title
        page = driver.page_source
        tried=0
        target = ''
        while len(target)==0 and tried<maxtry:
            time.sleep(3)
            target = page.find(searchflag)

        title = driver.title
        page = driver.page_source
        return title, page


accessbase = AccessBase()
