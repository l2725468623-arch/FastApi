"""SQLAlchemy 异步 MySQL 引擎与 FastAPI 数据库会话依赖。"""

import os
from pathlib import Path
from typing import AsyncIterator

from dotenv import load_dotenv
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv(Path(__file__).resolve().parents[1] / ".env", encoding="utf-8-sig")

ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL") or URL.create(
    "mysql+aiomysql",
    username=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", "123456"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "3306")),
    database=os.getenv("DB_NAME", "news_app"),
    query={"charset": "utf8mb4"},
)

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=os.getenv("DB_ECHO", "false").lower() == "true",
    pool_size=10,
    max_overflow=20,#连接池的数量
    pool_pre_ping=True,
)
#创建会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """所有 ORM 模型共用的基类。"""


async def get_db() -> AsyncIterator[AsyncSession]:
    """使用 Depends(get_db) 注入；写入数据后显式 await db.commit()。"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
