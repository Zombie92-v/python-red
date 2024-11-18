import json
import time



def extract_request_headers_and_body(driver, target_url_part,url , timeout=30, filter=None):
    """
    提取目标请求的 headers 和返回的 body 数据
    :param driver: WebDriver 实例
    :param target_url_part: 请求的 URL 关键字
    :param timeout: 超时时间（秒）
    :return: 请求的 URL 和解析后的 JSON 数据
    """
    driver.get(url)
    start_time = time.time()

    while time.time() - start_time < timeout:
        print(f"开始等待目标请求 '{target_url_part}'")
        logs = driver.get_log("performance")
        for entry in logs:
            try:
                log = json.loads(entry["message"])["message"]
                # 找到目标请求的发送
                if log["method"] == "Network.requestWillBeSent":
                    request = log["params"]["request"]
                    if target_url_part in request["url"]:
                        # 提取请求头
                        headers = request.get("headers", {})
                        print(f"请求头信息：{headers}")
                if log["method"] == "Network.responseReceived":
                    response = log["params"]["response"]
                    if target_url_part in response["url"]:
                        headers = None
                        try:
                            headers = json.loads(entry["message"])["message"]["params"]["response"]["headers"]
                            print("请求头", headers)
                        except Exception:
                            print("请求头解析失败")

                        print("content-type", headers.get("content-type", None))
                        if headers is None or (not filter and filter(headers)):
                            print("过滤掉")
                            continue
                        # 提取请求的 ID
                        request_id = log["params"]["requestId"]

                        # 获取完整的响应 body
                        response_body = driver.execute_cdp_cmd(
                            'Network.getResponseBody', {"requestId": request_id}
                        )

                        # 转为 JSON 格式
                        json_data = json.loads(response_body['body'])

                        print(f"目标请求完成：{response['url']}")
                        return response["url"], json_data
            except Exception as e:
                # 捕获解析错误或非 JSON 响应
                print(f"循环等待")
                continue
        time.sleep(1)  # 每秒轮询一次

    raise TimeoutError(f"等待目标请求 '{target_url_part}' 超时")


if __name__ == '__main__':
    from DriverManage import singleDriver
    driver = singleDriver.getDriver()
    print("""SDFsdf""")

    # 打开目标网页
    url = "https://www.xiaohongshu.com/explore/67346883000000001b010cfa?xsec_token=ABheASSYPcqzFhsmuUywUjdTz_Xmu0ftMnDmC_p-7gFg8=&xsec_source=pc_collect"  # 替换为目标网页 URL
    driver.get(url)

    # 定义目标请求的标识（例如 URL 的一部分）
    target_url_part = "/comment/page"  # 评论
    # target_url_part = "explore"  # 替换为你感兴趣的请求路径

    try:
        # 等待目标请求完成并获取 URL 和 JSON 数据
        target_url, json_response = extract_request_headers_and_body(driver, target_url_part, filter=lambda h: 'json' in h.get(
            "content-type"))

        print("目标请求的 URL：", target_url)
        response = json.loads(json.dumps(json_response, indent=4, ensure_ascii=False))
        for i in response['data']['comments']:
            print('评论内容：', i['content'])
            print('评论点赞数：', i['like_count'])
            print("评论人：", i['user_info'])
            pictures = i['pictures']
            if (len(pictures) > 0):
                print("评论图片:", i['pictures'][0]['url_pre'])

    finally:
        driver.quit()
    pass
