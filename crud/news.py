from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.news import Category


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Category]:
    stmt = select(Category).order_by(Category.sort_order, Category.id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())
