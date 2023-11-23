import os
from envparse import Env

env = Env()

DATABASE_URL = env.str(
    "DATABASE_URL",
    default=f"postgresql+asyncpg://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@"
    f"{os.environ.get('DATABASE')}:5432/{os.environ.get('POSTGRES_DB')}",
)