from pydantic import BaseModel


class RedContextReq(BaseModel):
    url: str
