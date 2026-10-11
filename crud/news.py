from typing import List, Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, update

from models.news import Category, News


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Category]:
    stmt = select(Category).order_by(Category.sort_order, Category.id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())





async def get_news_list(
    db: AsyncSession, category_id: int = 0, skip: int = 0, limit: int = 10
) -> Tuple[List[News], int]:
    stmt = select(News)
    count_stmt = select(func.count()).select_from(News)
    if category_id > 0:
        stmt = stmt.where(News.category_id == category_id)
        count_stmt = count_stmt.where(News.category_id == category_id)

    total = await db.scalar(count_stmt) or 0
    stmt = stmt.order_by(News.publish_time.desc(), News.id.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all()), total



async def get_news_detail(db: AsyncSession, news_id: int) -> Tuple[Optional[News], List[News]]:

    result = await db.execute(select(News).where(News.id == news_id))
    article = result.scalars().one_or_none()
    if article is None:
        return None, []

    related_stmt = (
        select(News)
        .where(News.category_id == article.category_id, News.id != article.id)
        .order_by(News.publish_time.desc(), News.id.desc())
        .limit(5)
    )
    related_result = await db.execute(related_stmt)
    return article, list(related_result.scalars().all())



async def getnews(db: AsyncSession, skip: int = 0, limit: int = 100) -> Tuple[List[News], int]:
    stmt = select(News).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return  result.scalars().one_or_none()

async def increase_news_views(db: AsyncSession, news_id: int) -> int:
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    await db.execute(stmt)
    await db.commit()
    return await db.scalar(select(News.views).where(News.id == news_id)) or 0

