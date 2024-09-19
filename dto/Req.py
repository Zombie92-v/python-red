from pydantic import BaseModel


# 小红书链接
class RedContextReq(BaseModel):
    url: str
