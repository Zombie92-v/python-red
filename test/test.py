from requests.api import get
from dto.resp import *
from bs4 import BeautifulSoup


def red_spider_chromeBy(url=''):
    """爬取视频 图片 """
    url = get(url)
    text = url.content
    soup = BeautifulSoup(text, "html.parser")
    res = RedContextResp()
    # 解析图片
    masterImgList = []
    try:
        list = soup.select("meta[name='og:image']")
        for i in list:
            masterImgList.append(i["content"])
    except Exception as e:
        print(e)
    res.masterImgList = masterImgList;
    # 解析视频
    mp4List = []
    try:
        list = soup.select("meta[name='og:video']")
        for i in list:
            mp4List.append(i["content"])
    except Exception as e:
        print(e)
    res.mp4List = mp4List
    # 解析标题 关键字 内容描述
    try:
        title = soup.select_one("meta[name='og:title']")
        res.title = title["content"]
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
    res = red_spider_chromeBy(
        "https://www.xiaohongshu.com/explore/66e5dfed0000000012010cc9?xsec_token=ABDkT-9Pi2lAeSysxHHtCZDJB1QCXfl35EeeLy7LogLkY=&xsec_source=pc_feed")
    print(res)
