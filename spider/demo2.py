# coding=utf8
from selenium import webdriver  # 导入webdriver包

import time
from bs4 import BeautifulSoup


driver = webdriver.Firefox()  # 初始化一个火狐浏览器实例：driver

driver.maximize_window()  # 最大化浏览器

time.sleep(5)  # 暂停5秒钟

url = 'https://www.qichacha.com/search?key=91210800MA0QCLUT14'
c=  driver.get("https://www.baidu.com")  # 通过get()方法，打开一个url站点
soup = BeautifulSoup(c, 'lxml')
pass

