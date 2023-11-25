from fastapi import Depends, HTTPException, APIRouter
from api.actions.users import _create_user, _change_password_user
from api.users.schemas import ShowUser, CreateUser, ChangePasswordUser
from db.session import AsyncSession, get_db

user_router = APIRouter()

@user_router.post("/reg", response_model=ShowUser)
async def create_user(body: CreateUser, db: AsyncSession = Depends(get_db)) -> ShowUser:
    """Registration user"""
    user = await _create_user(body, db)
    if user is None:
        raise HTTPException(status_code=400, detail="this login is already exists")
    return user

@user_router.put("/change_password", response_model=ShowUser)
async def change_password_user(body: ChangePasswordUser, db: AsyncSession = Depends(get_db)) -> ShowUser:
    """change password of user"""
    user = await _change_password_user(body, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user