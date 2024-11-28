from selenium.webdriver.common.by import By

from DriverManage import singleDriver
from Tools import *
from dto.resp import *


def red_spider_chrome(url=''):
    url = parseUrl(url)
    res = RedContextResp()
    try:

        pageHtml = singleDriver.getPage(url)
        res.mp4List = parseMp4(pageHtml)
        driver = singleDriver.getDriver()
        imgList = []
        try:
            list = driver.find_elements(By.CSS_SELECTOR, "meta[name='og:image']")
            for i in list:
                imgList.append(convert_http_to_https(i.get_attribute('content')))
        except Exception as e:
            print(e)
        res.masterImgList = imgList
        # 解析标题 关键字 内容描述
        try:
            title = driver.find_element(By.CSS_SELECTOR, "meta[name='og:title']")
            res.title = title.get_attribute('content')
        except Exception as e:
            print(e)
        # 解析关键字
        try:
            keywords = driver.find_element(By.CSS_SELECTOR, "meta[name='keywords']")
            res.keywords = keywords.get_attribute('content')
        except Exception as e:
            print(e)
        # 解析内容描述
        try:
            description = driver.find_element(By.CSS_SELECTOR, "meta[name='description']")
            res.description = description.get_attribute('content')
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)
    finally:
        # 设置为空页面
        singleDriver.openBlank()
    return res
if __name__ == '__main__':
    res = red_spider_chrome(
        url="https://www.xiaohongshu.com/explore/67346883000000001b010cfa?xsec_token=ABheASSYPcqzFhsmuUywUjdTz_Xmu0ftMnDmC_p-7gFg8=&xsec_source=pc_collect")
    print(res)
