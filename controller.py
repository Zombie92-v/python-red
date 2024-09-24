from fastapi import FastAPI

from dto.req import *
from dto.resp import suc
from spider_google import red_spider_chrome
from spider_by_requests import red_spider_requests

app = FastAPI()



@app.get("/")
async def read_root():
    return {"Hello": "red"}


@app.on_event("shutdown")
def shutdown():
    print("shutting down")


@app.post("/red/context")
async def redContext(req: RedContextReq):
    if(req.type=='mata'):
        return suc(red_spider_requests(req.url))
    return suc(red_spider_chrome(url=req.url))
