from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from config.database import async_engine
from routers import news


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        await async_engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return FileResponse(Path(__file__).resolve().parent / "web" / "index.html")


app.include_router(news.router)

# 启动入口：支持直接点击 PyCharm 运行按钮启动服务
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("demo:app", host="127.0.0.1", port=8000, reload=True)
