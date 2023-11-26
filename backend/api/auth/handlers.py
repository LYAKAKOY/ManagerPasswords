from datetime import timedelta

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

import settings
from JWT import create_access_token
from api.actions.auth import authenticate_user
from api.auth.schemas import Token
from api.users.handlers import user_router
from db.session import AsyncSession, get_db


@user_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.user_id), "other_custom_data": []},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")