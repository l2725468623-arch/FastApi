from fastapi import FastAPI
from typing import Optional
from routers import news
from contextlib import asynccontextmanager
from config.database import async_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        await async_engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}
app.include_router(news.router)
#挂载路由

# 启动入口：支持直接点击PyCharm运行按钮启动服务
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("demo:app", host="127.0.0.1", port=8000, reload=True)
