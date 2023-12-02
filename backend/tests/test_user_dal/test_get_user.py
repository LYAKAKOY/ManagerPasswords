import pytest
from db.users.user_dal import UserDAL
from hashing import Hasher
from tests.conftest import create_user


@pytest.mark.parametrize(
    "login, password",
    [
        ("login1", "password1"),
    ],
)
async def test_get_user_by_user_id(async_session_test, asyncpg_pool, login, password):
    session = async_session_test()
    user = await create_user(asyncpg_pool, login=login, password=password)
    async with session.begin():
        user_dal = UserDAL(session)
        got_user = await user_dal.get_user_by_user_id(user_id=user["user_id"])
    assert user["user_id"] == got_user.user_id
    assert login == got_user.login
    assert Hasher.verify_password(password, got_user.password)


@pytest.mark.parametrize(
    "login, password",
    [
        ("login1", "password1"),
    ],
)
async def test_get_user_by_login(async_session_test, asyncpg_pool, login, password):
    session = async_session_test()
    user = await create_user(asyncpg_pool, login=login, password=password)
    async with session.begin():
        user_dal = UserDAL(session)
        got_user = await user_dal.get_user_by_login(login=login)
    assert user["user_id"] == got_user.user_id
    assert login == got_user.login
    assert Hasher.verify_password(password, got_user.password)
