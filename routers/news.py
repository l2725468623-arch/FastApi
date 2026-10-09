from fastapi import APIRouter


#创建Apirouter 实例
router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/categories")
async def get_categories():
    return {"msg":"获取分类success"}



