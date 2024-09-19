from fastapi import FastAPI
from spider import red_spider
from spider_google import red_spider_chrome
from dto.Req import *

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/red")
async def read_item(req: RedContextReq):
    return red_spider(req.url)

@app.post("/red/chrome")
async def read_item_chrome(req: RedContextReq):
    return red_spider_chrome(req.url)