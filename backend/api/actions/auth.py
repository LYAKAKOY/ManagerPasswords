import uuid

import settings
from db.session import get_db
from db.users.models import User
from db.users.user_dal import UserDAL
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from hashing import Hasher
from jose import jwt
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def _get_user_by_user_id_for_auth(
    user_id: uuid.UUID, session: AsyncSession
) -> User | None:
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_user_id(user_id=user_id)


async def _get_user_by_login_for_auth(login: str, session: AsyncSession) -> User | None:
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_login(login=login)


async def authenticate_user(login: str, password: str, db: AsyncSession) -> User | None:
    if (user := await _get_user_by_login_for_auth(login=login, session=db)) is None:
        return
    if not Hasher.verify_password(password, user.password):
        return
    return user


async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await _get_user_by_user_id_for_auth(user_id=user_id, session=db)
    if user is None:
        raise credentials_exception
    return user
