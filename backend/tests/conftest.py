import asyncio
import os
import uuid
from typing import Any
from typing import Callable
from typing import Generator

import asyncpg
import pytest
import settings
from crypting import AES
from cryptography.fernet import Fernet
from db.session import get_db
from hashing import Hasher
from httpx import AsyncClient
from JWT import create_access_token
from main import app
from sqlalchemy import text
from tests.db_test import async_session

CLEAN_TABLES = ["users"]


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
    await pool.close()


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(
                    text(f"TRUNCATE TABLE {table_for_cleaning} CASCADE ")
                )


@pytest.fixture(scope="function")
async def create_user(asyncpg_pool):
    async def get_user_fields(login: str = "login", password: str = "password"):
        user_id = uuid.uuid4()
        aes_key = Fernet.generate_key()
        async with asyncpg_pool.acquire() as connection:
            await connection.execute(
                """INSERT INTO users VALUES ($1, $2, $3, $4)""",
                user_id,
                login,
                Hasher.get_password_hash(password),
                aes_key,
            )
            return {"user_id": user_id, "aes_key": aes_key}

    return get_user_fields


@pytest.fixture
async def create_service_password(asyncpg_pool, create_user: Callable) -> Callable:
    async def create_password(
        service: str, password: str, user_id: uuid.UUID, aes_key: bytes
    ):
        async with asyncpg_pool.acquire() as connection:
            aes = AES(aes_key)
            await connection.execute(
                """INSERT INTO passwords (service_name, password, user_id) VALUES ($1, $2, $3)""",
                service,
                aes.encrypt_password(password),
                user_id,
            )

    return create_password


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


def get_test_auth_headers_for_user(user_id: uuid.UUID):
    access_token = create_access_token(
        data={"sub": str(user_id), "other_custom_data": []}
    )
    return {"Authorization": f"Bearer {access_token}"}
