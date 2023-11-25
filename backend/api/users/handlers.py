from fastapi import Depends, HTTPException, APIRouter
from api.actions.users import _create_user
from api.users.schemas import ShowUser, CreateUser
from db.session import AsyncSession, get_db

user_router = APIRouter()

@user_router.post("/reg", response_model=ShowUser)
async def create_user(user: CreateUser, db: AsyncSession = Depends(get_db)) -> ShowUser:
    """Registration user"""
    user = await _create_user(user, db)
    if user is None:
        raise HTTPException(status_code=400, detail="this login is already exists")
    return user