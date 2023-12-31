import os
from typing import List

from envparse import Env

env = Env()

DATABASE_URL = env.str(
    "DATABASE_URL",
    default=f"postgresql+asyncpg://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@"
    f"{os.environ.get('DATABASE')}:{os.environ.get('POSTGRES_PORT')}/{os.environ.get('POSTGRES_DB')}",
)

SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")
ALGORITHM: str = env.str("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)

ALLOW_ORIGINS: List = env.list(
    "ALLOW_ORIGINS",
    default=[
        "http://localhost",
        "http://localhost:8000",
    ],
)

SENTRY_URL: str = env.url(
    "SENTRY_URL",
    default="https://eec20034949b2b27dc10652f4cef5d46@o4506314416521216.ingest.sentry.io/4506314420649984",
)
