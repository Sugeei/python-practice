# https://stackoverflow.com/questions/11450158/how-do-i-set-proxy-for-chrome-in-python-webdriver

from selenium import webdriver

PROXY = "23.23.23.23:3128" # IP:PORT or HOST:PORT

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)

chrome = webdriver.Chrome(options=chrome_options)
chrome.get("http://whatismyipaddress.com")



from selenium import webdriver

PROXY = "23.23.23.23:3128" # IP:PORT or HOST:PORT

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=http://%s' % PROXY)

chrome = webdriver.Chrome(chrome_options=chrome_options)
chrome.get("http://whatismyipaddress.com")