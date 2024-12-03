from pydantic import BaseModel


# 小红书链接
class RedContextReq(BaseModel):
    url: str
    type: str = None


class RedChatReq(BaseModel):
    txt: str


class RedImgIdReq(BaseModel):
    img_ids: list
    prd: int = 0
