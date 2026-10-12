from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import user
from config.database import get_db
router = APIRouter(prefix="/api/user", tags=["user"])



@router.post("/register")
async def register(user_data: user.UserRequest, db:AsyncSession = Depends(get_db)):
    return {
    "code": 200,
    "message": "注册成功",
    "data": {
        "token":"用户访问令牌",
        "userInfo": {
        "id": 1,
        "username":user_data.username ,
        "bio":"这个人很懒,什么都没留下",
    "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
    }
 }
    }