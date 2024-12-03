import uvicorn

if __name__ == '__main__':
    # 运行fastapi程序
    uvicorn.run(app="controller:app", host="0.0.0.0", port=8000, reload=True)
