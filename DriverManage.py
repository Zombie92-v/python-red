import sys

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from FakeUserAgentManage import ua
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class SingletonDriver:
    driver = None

    def __init__(self):
        if sys.platform.startswith('linux'):
            service = Service(executable_path="./driver/chromedriver", log_path=os.devnull)
        else:
            service = Service(executable_path="./driver/chromedriver.exe", log_path=os.devnull)
        options = webdriver.ChromeOptions()
        options.use_chromium = True

        # 设置参数
        No_Image_loading = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", No_Image_loading)
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches', ['enable-automation','enable-logging'])

        # 设置无头参数
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('window-size=1920,1080')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-infobars')
        options.add_argument("--remote-allow-origins=*")
        options.add_argument('--no-sandbox')  # 给予root执行权限
        options.add_argument('--disable-extensions')  # 禁止拓展
        # 设置隐私模式（无痕模式）
        # options.add_argument('--incognito')
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/10.130.24.142 Safari/537.36')
        # 启用性能日志捕获
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        try:
            self.driver = webdriver.Chrome(service=service, options=options, desired_capabilities=capabilities)
        except Exception as e:
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options, desired_capabilities=capabilities)
    def getDriver(self):
        return self.driver
    def getPage(self,url):
        # 启用网络调试功能
        self.driver.execute_cdp_cmd('Network.enable', {})
        # 使用 DevTools 设置用户代理和其他请求头
        userAgent = ua.chrome
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": f"{userAgent}",  # 设置自定义 User-Agent
        })
        self.driver.get(url)
        return self.driver.page_source
    def openBlank(self):
        self.driver.get("about:blank")

singleDriver = SingletonDriver()

if __name__ == '__main__':
    singleDriver.getPage("https://www.xiaohongshu.com/explore/64bca652000000000a01a9e5?xsec_token=ABkhybo7OApw6qBnXqJZxRsetwxPr42h0jTrhZ2JR0aZE=&xsec_source=pc_search")