from api.actions.auth import get_current_user_from_token
from api.actions.users import _change_master_password_user
from api.actions.users import _change_password_user
from api.actions.users import _create_user
from api.users.schemas import ChangePasswordUser
from api.users.schemas import CreateUser
from api.users.schemas import ShowUser
from db.session import AsyncSession
from db.session import get_db
from db.users.models import User
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

user_router = APIRouter()


@user_router.post("/reg", response_model=ShowUser)
async def create_user(body: CreateUser, db: AsyncSession = Depends(get_db)) -> ShowUser:
    """Registration user"""
    user = await _create_user(body, db)
    if user is None:
        raise HTTPException(status_code=422, detail="this login is already exists")
    return user


@user_router.put("/change_password", response_model=ShowUser)
async def change_password_user(
    body: ChangePasswordUser, db: AsyncSession = Depends(get_db)
) -> ShowUser:
    """change password of user"""
    user = await _change_password_user(body, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@user_router.put("/change_master_password", response_model=ShowUser)
async def change_master_password_user(
    current_user: User = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db),
) -> ShowUser:
    """change master password of user"""
    user = await _change_master_password_user(current_user, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
