import asyncio
import os
import uuid
from typing import Generator, Any

import asyncpg
from httpx import AsyncClient
import pytest
from sqlalchemy import text

import settings
from crypting import AES
from db.passwords.models import HexByteString
from db.session import get_db
from main import app
from tests.db_test import async_session

CLEAN_TABLES = ['users']

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
def run_migrations():
    os.system("alembic upgrade heads")

@pytest.fixture(scope="session")
async def async_session_test():
    yield async_session

@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool("".join(settings.DATABASE_URL.split("+asyncpg")))
    yield pool
    pool.close()


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(text(f"TRUNCATE TABLE {table_for_cleaning} CASCADE "))
@pytest.fixture(scope="function")
async def create_user(asyncpg_pool):
    user_id = uuid.uuid4()
    async with asyncpg_pool.acquire() as connection:
        await connection.execute(
            """INSERT INTO users VALUES ($1, $2, $3)""",
            user_id,
            "login",
            str(AES.encrypt_password("password")),
        )
        return user_id

async def _get_test_db():
    async with async_session() as session:
        yield session

@pytest.fixture(scope="function")
async def client() -> Generator[AsyncClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `get_db` fixture to override
    the `get_db` dependency that is injected into routes.
    """
    app.dependency_overrides[get_db] = _get_test_db
    async with AsyncClient(app=app, base_url="http://127.0.0.1") as client:
        yield client
