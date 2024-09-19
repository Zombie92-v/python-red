from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from Tools import parseMp4
from selenium.webdriver.common.by import By
from dto.Resp import *
import sys
if sys.platform.startswith('linux'):
    service = Service(executable_path="chromedriver")
else:
    service = Service(executable_path="chromedriver.exe")
options = webdriver.ChromeOptions()
options.use_chromium = True

# 设置参数
No_Image_loading = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", No_Image_loading)
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('excludeSwitches', ['enable-automation'])

# 设置无头参数
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('window-size=1920x1080')
options.add_argument('--start-maximized')
options.add_argument('--disable-infobars')
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36')
def red_spider_chrome(url=''):
    driver = webdriver.Chrome(service=service,options=options)
    res = RedContextResp()
    try:
        driver.get(url)
        pageHtml = driver.page_source

        res.mp4List = parseMp4(pageHtml)

        imgList = []
        try:
            list = driver.find_elements(By.CSS_SELECTOR, "meta[name='og:image']")
            for i in list:
                imgList.append(i.get_attribute('content'))
        except Exception as e:
            print(e)
        res.masterImgList = imgList
    finally:
        driver.quit()
    return res
