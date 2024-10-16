import os
from http.client import HTTPException


from dto.req import *
from dto.resp import suc
from spider_google import red_spider_chrome
from spider_by_requests import red_spider_requests
from chat import *
from fastapi import FastAPI, HTTPException,Request,Response
from fastapi.responses import FileResponse
from pathlib import Path
import time
import json


from logUtil import log

app = FastAPI()

# 为app增加接口处理耗时的响应头信息
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # 记录请求开始时间
    start_time = time.time()

    # 获取请求信息
    method = request.method
    url = request.url.path
    client_host = request.client.host
    query_params = request.url.query

    # 记录基础请求信息
    body_pretty = None
    if method == "POST":
        try:
            # 读取请求体
            body_bytes = await request.body()
            body_str = body_bytes.decode('utf-8')
            # 尝试解析为JSON格式，便于阅读
            try:
                body_json = json.loads(body_str)
                body_pretty = json.dumps(body_json, indent=2, ensure_ascii=False,separators=(',', ':'))
            except json.JSONDecodeError:
                # 如果不是JSON格式，直接记录原始字符串
                body_pretty = body_str
        except Exception as e:
            log(f"读取请求体时出错: {e}")

    log(f"请求开始: {method} {url} 来自 {client_host} 查询参数: {query_params} 请求体:{body_pretty}")
    try:
        # 处理请求
        response: Response = await call_next(request)
    except Exception as e:
        # 记录异常信息
        log(f"请求处理出错: {e}")
        raise e

    # 记录请求处理时间和响应状态码
    process_time = (time.time() - start_time) * 1000  # 毫秒
    status_code = response.status_code

    log(f"请求完成: {method} {url} 状态码 {status_code} 用时 {process_time:.2f}ms")

    return response

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