from datetime import datetime
from datetime import timedelta

import settings
from jose import jwt


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    time_now = datetime.utcnow()
    if expires_delta:
        expire = time_now + expires_delta
    else:
        expire = time_now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": time_now})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
