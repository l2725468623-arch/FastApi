from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_db
from crud import news


router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/categories")
async def get_categories(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    categories = await news.get_categories(db, skip, limit)
    return {
        "code": 200,
        "message": "获取新闻分类成功",
        "data": [
            {
                "id": category.id,
                "name": category.name,
                "sort_order": category.sort_order,
                "created_at": category.created_at,
                "updated_at": category.updated_at,
            }
            for category in categories
        ],
    }
@router.get("/list")
async def get_news_list(
        category_id: int = Query(default=0, alias="categoryid"),
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=20, alias="pagesize",le=100),
        db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * page_size
    news_list, total = await news.get_news_list(db, category_id, offset, page_size)
    has_more = (offset + len(news_list)) < total
    return {
        "code": 200,
        "message":"success",
        "data": {
            "list":news_list,
            "total":total,
            "hasmore":has_more,

        }
    }

@router.get("/detail")
async def get_news_detail(
    news_id: int = Query(..., alias="newsId", gt=0),
    db: AsyncSession = Depends(get_db),
):
    article, related_news = await news.get_news_detail(db, news_id)
    if article is None:
        raise HTTPException(status_code=404, detail="新闻不存在")
    views = await news.increase_news_views(db, article.id)
    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "image": article.image,
            "author": article.author,
            "publishTime": article.publish_time,
            "categoryId": article.category_id,
            "views": views,
            "relatedNews": [
                {
                    "id": item.id,
                    "title": item.title,
                    "image": item.image,
                    "author": item.author,
                    "publishTime": item.publish_time,
                    "views": item.views,
                }
                for item in related_news
            ],
        }
    }
