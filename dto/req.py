from pydantic import BaseModel


# 小红书链接
class RedContextReq(BaseModel):
    url: str
    type: str = None
class RedChatReq(BaseModel):
    txt: str
