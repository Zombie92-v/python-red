import os
from http.client import HTTPException


from dto.req import *
from dto.resp import suc
from spider_google import red_spider_chrome
from spider_by_requests import red_spider_requests
from chat import *
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()



@app.get("/")
async def read_root():
    return {"Hello": "red"}


@app.on_event("shutdown")
def shutdown():
    print("shutting down")


@app.post("/red/context")
async def redContext(req: RedContextReq):
    if(req.type=='all'):
        return suc(red_spider_chrome(url=req.url))
    return suc(red_spider_requests(req.url))

@app.post("/red/chat")
async def redChat(req: RedChatReq):
    return suc(chat_gemma(req.txt))


@app.get("/file/{filename}")
async def get_video(filename: str):
    """
    提供访问本地 MP4 文件的 URL。
    """
    # 确保请求的文件存在于媒体目录中
    # 定义存储媒体文件的目录
    MEDIA_DIR = Path("downloads")
    file_path = MEDIA_DIR / filename
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="文件未找到")

    return FileResponse(path=file_path, media_type="file/mp4", filename=filename)