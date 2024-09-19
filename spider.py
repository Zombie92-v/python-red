from selenium import webdriver
from selenium.webdriver.edge.service import Service
from Tools import parseMp4
from selenium.webdriver.common.by import By
from dto.Resp import *

import time

service = Service(executable_path="msedgedriver.exe")
Edge_options = webdriver.EdgeOptions()
Edge_options.use_chromium = True

# 设置参数
No_Image_loading = {"profile.managed_default_content_settings.images": 2}
Edge_options.add_experimental_option("prefs", No_Image_loading)
Edge_options.add_experimental_option('useAutomationExtension', False)
Edge_options.add_experimental_option('excludeSwitches', ['enable-automation'])
Edge_options.add_experimental_option('excludeSwitches', ['enable-automation'])

# 设置无头参数
# Edge_options.add_argument('--headless')
Edge_options.add_argument('--disable-gpu')
Edge_options.add_argument('window-size=1920x1080')
Edge_options.add_argument('--start-maximized')
Edge_options.add_argument('--disable-infobars')
Edge_options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36')

def red_spider(url=''):
    driver = webdriver.Edge(service=service,options=Edge_options)
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
