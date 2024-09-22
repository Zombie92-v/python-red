from bs4 import BeautifulSoup
import json
import re

def parseUrl(text=None):
    # 正则表达式匹配URL
    url_pattern = r'(https?://[^\s,，]+)'
    url = re.findall(url_pattern, text)
    if(len(url)==0):
        return text
    return url[0]

def traverse_json(data, search=None, res=[]):
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                traverse_json(v, search, res)
            else:
                if search == k:
                    res.append(v)
    elif isinstance(data, list):
        for item in data:
            traverse_json(item, search, res)


def parseMp4(page):
    mp4List=[]
    try:
        bsObj = BeautifulSoup(page, 'html.parser')
        bsElems = bsObj.find_all('script')

        for bsElem in bsElems:
            if bsElem.text.find("window.__INITIAL_STATE__") >= 0:
                scriptData = bsElem.text.lstrip("window.__INITIAL_STATE__=")
                scriptData = scriptData.replace("undefined", "\"\"")
                jsonData = json.loads(str(scriptData))
                traverse_json(jsonData, search="masterUrl", res=mp4List)
    except Exception as e:
        print(e)
    return mp4List