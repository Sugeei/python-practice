import scrapy
import pymongo
import re, os
from onlineCourse.items import ITEMKEYS, BosssPositionItem, PosInfoItem
from scrapy.conf import settings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from scrapy.selector import Selector


# https://www.baidu.com/s?wd="大数据 培训"

def writeFile(dirPath, page):
    data = Selector(text = page).xpath("//td[@class='zwmc']/div/a")
    titles = data.xpath('string(.)').extract()
    timeMarks = Selector(text = browser.page_source).xpath("//td[@class='gxsj']/span/text()").extract()
    links = Selector(text = browser.page_source).xpath("//td[@class='zwmc']/div/a/@href").extract()

    for i in range(len(titles)):
        fileName = titles[i].replace(':', '-').replace('/', '-').replace('\\', '-').replace('*', 'x').replace('|', '-').replace('?', '-').replace('<', '-').replace('>', '-').replace('"', '-').replace('\n', '-').replace('\t', '-')
        filePath = dirPath + os.sep + fileName + '.txt'

        with open(filePath, 'w') as fp:
            fp.write(titles[i])
            fp.write('$***$')
            fp.write(timeMarks[i])
            fp.write('$***$')
            fp.write(links[i])


def searchFunction(browser, url, keyWord, dirPath):
    browser.get(url)
    #
    # # input
    # browser.find_element_by_xpath("//input[@id='s_ipt']").click()
    # browser.find_element_by_xpath("//table[@class='sPopupTabC']/tbody/tr[1]/td/label/input[@iname='北京']").click()
    # browser.find_element_by_xpath("//table[@class='sPopupTabC']/tbody/tr[1]/td/label/input[@iname='上海']").click()
    # browser.find_element_by_xpath("//table[@class='sPopupTabC']/tbody/tr[3]/td/label/input[@iname='南京']").click()
    # browser.find_element_by_xpath("//table[@class='sPopupTabC']/tbody/tr[4]/td/label/input[@iname='苏州']").click()
    # browser.find_element_by_xpath("//table[@class='sPopupTabC']/tbody/tr[4]/td/label/input[@iname='无锡']").click()
    # browser.find_element_by_xpath("//div[@class='sPopupTitle250']/div/a[1]").click()

    #定位搜索框
    searchBox = browser.find_element_by_xpath("//input[@class='s_ipt']")

    #发送搜索内容
    searchBox.send_keys(keyWord)

    #确认搜索
    browser.find_element_by_xpath("//input[@type='submit']").click()

    title = Selector(text = browser.page_source).xpath('//div[@class="ZQDxnR"]/h3[@class="t ghpBWq TWjHxp"]/a/text()').extract()[0]

    writeFile(dirPath, title)



if __name__ == '__main__':
    # print 'START'
    url = 'https://www.baidu.com/'
    keyWord = u"大数据 培训"
    dirPath = os.getcwd() + 'bigdata_training_info.txt'

    # if not os.path.exists(dirPath):
    #     os.makedirs(dirPath)

    #定义一个浏览器对象
    #browser = webdriver.Firefox()
    browser = webdriver.PhantomJS()
    searchFunction(browser, url, keyWord, dirPath)

    browser.close()
    # print 'END'