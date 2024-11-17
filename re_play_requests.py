import json
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def extract_request_details(driver, target_url_part, timeout=30):
    """
    提取目标请求的 headers、body 和 method 数据
    :param driver: WebDriver 实例
    :param target_url_part: 请求的 URL 关键字
    :param timeout: 超时时间（秒）
    :return: 请求的 URL、请求头、请求体、请求类型
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        logs = driver.get_log("performance")
        for entry in logs:
            try:
                log = json.loads(entry["message"])["message"]

                # 找到目标请求的发送
                if log["method"] == "Network.requestWillBeSent":
                    request = log["params"]["request"]
                    if target_url_part in request["url"]:
                        headers = request.get("headers", {})
                        body = request.get("postData", None)  # 请求体，可能为 None
                        method = request.get("method", "GET")
                        url = request["url"]

                        print(f"请求头：{headers}")
                        print(f"请求体：{body}")
                        print(f"请求类型：{method}")
                        if method != 'GET' and method != 'POST':
                            continue
                        print(f"请求 URL: {url}")
                        headers["Cookie"] = get_cookies_as_header(driver)
                        return url, headers, body, method

            except Exception as e:
                print(f"解析错误: {e}")
                continue
        time.sleep(1)

    raise TimeoutError(f"等待目标请求 '{target_url_part}' 超时")


def replay_request(url, headers, body, method):
    """
    使用 requests 重播请求
    :param url: 请求的 URL
    :param headers: 请求头
    :param body: 请求体
    :param method: 请求方法
    :return: 请求的响应数据
    """
    proxies = {
        "http": None,
        "https": None,
    }
    headers["User-Agent"] = "PostmanRuntime/7.42.0"
    headers["Accept"] = "*/*"
    headers[
        "User-Agent"] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    print(headers)
    try:
        from urllib.parse import quote
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, proxies=proxies)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, data=body)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, data=body)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, data=body)
        else:
            raise ValueError(f"不支持的请求方法: {method}")

        response.raise_for_status()
        return response.text

    except requests.RequestException as e:
        print(f"请求失败：{e}")
        return None


def get_cookies_as_header(driver):
    """
    从 Selenium 获取当前页面的 Cookie，并格式化为请求头的 'Cookie' 字段
    :param driver: WebDriver 实例
    :return: 格式化的 Cookie 字符串
    """
    cookies = driver.get_cookies()
    cookie_header = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    return cookie_header


# 示例流程
if __name__ == "__main__":
    # 启动 WebDriver
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    service = Service("driver/chromedriver.exe")
    driver = webdriver.Chrome(service=service, desired_capabilities=capabilities)

    try:
        # 打开目标网页
        url = "https://www.xiaohongshu.com/explore/67346883000000001b010cfa?xsec_token=ABheASSYPcqzFhsmuUywUjdTz_Xmu0ftMnDmC_p-7gFg8=&xsec_source=pc_collect"
        driver.get(url)

        # 提取请求的详情
        target_url_part = "/comment/page"
        target_url, headers, body, method = extract_request_details(driver, target_url_part)

        # 重播请求
        replay_response = replay_request(target_url, headers, body, method)
        print("重播请求的返回数据：", replay_response)

    finally:
        driver.quit()
