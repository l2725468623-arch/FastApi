from datetime import datetime

from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class Category(Base):
    """新闻分类。"""

    __tablename__ = "news_category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="分类ID")
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="分类名称")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="排序")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False, comment="更新时间"
    )

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name={self.name!r}, sort_order={self.sort_order})>"


class News(Base):
    """新闻文章。"""

    __tablename__ = "news"
    __table_args__ = (
        Index("fk_news_category_idx", "category_id"),#高频场景
        Index("idx_publish_time", "publish_time"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="新闻ID")
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="新闻标题")
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="新闻描述")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="新闻内容")
    image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="封面图片URL")
    author: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="作者")
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("news_category.id"), nullable=False, comment="分类ID"
    )
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="浏览量")
    publish_time: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False, comment="发布时间"
    )

    def __repr__(self) -> str:
        return f"<News(id={self.id}, title={self.title!r}, views={self.views})>"
