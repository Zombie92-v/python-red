from bs4 import BeautifulSoup
from requests.api import get

from Tools import *
from dto.resp import *


def red_spider_requests(url=''):
    """爬取视频 图片 """
    url = parseUrl(url)
    url = get(url, proxies={"http": None, "https": None})
    text = url.content
    soup = BeautifulSoup(text, "html.parser")
    print(soup)
    res = RedContextResp()
    # 解析图片
    masterImgList = []
    try:
        image = soup.select("meta[name='og:image']")
        for i in image:
            masterImgList.append(i["content"])
    except Exception as e:
        print(e)
    res.masterImgList = list(map(lambda item: convert_http_to_https(item), masterImgList))
    # 解析视频
    mp4List = []
    try:
        image = soup.select("meta[name='og:video']")
        for i in image:
            url = i["content"]
            mp4List.append(url)
    except Exception as e:
        print(e)
    res.mp4List = list(map(lambda item: convert_http_to_https(item), mp4List))
    # 解析标题 关键字 内容描述
    try:
        title = soup.select_one("meta[name='og:title']")
        res.title = title["content"].replace("小红书", "").replace("-", "").strip()
    except Exception as e:
        print(e)
    # 解析关键字
    try:
        keywords = soup.select_one("meta[name='keywords']")
        res.keywords = keywords["content"]
    except Exception as e:
        print(e)
    # 解析内容描述
    try:
        description = soup.select_one("meta[name='description']")
        res.description = description["content"]
    except Exception as e:
        print(e)
    finally:
        return res


if __name__ == '__main__':
    res = red_spider_requests(
        "https://www.xiaohongshu.com/explore/67398893000000003c01caa2?xsec_token=ABAO1yC5N281L2A4EHaHNrUC9ZeLuBhbDD3plJXSWAKbo=&xsec_source=pc_feed")
    print(res.mp4List)
