import sys

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class SingletonDriver:
    driver = None

    def __init__(self):
        if sys.platform.startswith('linux'):
            service = Service(executable_path="./driver/chromedriver")
        else:
            service = Service(executable_path="./driver/chromedriver.exe")
        options = webdriver.ChromeOptions()
        options.use_chromium = True

        # 设置参数
        No_Image_loading = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", No_Image_loading)
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('excludeSwitches', ['enable-automation'])

        # 设置无头参数
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('window-size=450*450')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-infobars')
        options.add_argument("--remote-allow-origins=*")
        options.add_argument('--no-sandbox')  # 给予root执行权限
        options.add_argument('--disable-extensions')  # 禁止拓展
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36')
        try:
            self.driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)


driver = SingletonDriver().driver
