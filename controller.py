from fastapi import FastAPI

from dto.Req import *
from spider_google import red_spider_chrome

app = FastAPI()



@app.get("/")
async def read_root():
    return {"Hello": "red"}


@app.on_event("shutdown")
def shutdown():
    print("shutting down")


@app.post("/red/context")
async def redContext(req: RedContextReq):
    return red_spider_chrome(req.url)
