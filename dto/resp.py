# 小红书数据返回
class RedContextResp:
    masterImgList: []
    mp4List: []
    title: str
    description: str
    keywords: str

class Resp:
    code = 200
    data : {}
    message: ""
    result: None

def suc(result):
    response = Resp()
    response.code = 200
    response.message = 'success'
    response.result = result
    return response