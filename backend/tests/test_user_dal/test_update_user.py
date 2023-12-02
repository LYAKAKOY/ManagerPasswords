import pytest
from db.users.user_dal import UserDAL
from hashing import Hasher
from tests.conftest import create_user


@pytest.mark.parametrize(
    "login, password, new_password",
    [
        ("login1", "password1", "new_password1"),
    ],
)
async def test_update_user_password(
    async_session_test, asyncpg_pool, login, password, new_password
):
    session = async_session_test()
    await create_user(asyncpg_pool, login=login, password=password)
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.set_password(
            login=login, password=Hasher.get_password_hash(new_password)
        )
        assert Hasher.verify_password(new_password, user.password)
        assert user.login == login


@pytest.mark.parametrize(
    "login, password",
    [
        ("login1", "password1"),
    ],
)
async def test_update_user_master_password(
    async_session_test, asyncpg_pool, login, password
):
    session = async_session_test()
    user1 = await create_user(asyncpg_pool, login=login, password=password)
    async with session.begin():
        user_dal = UserDAL(session)
        user2 = await user_dal.generate_new_master_password(user_id=user1["user_id"])
        assert Hasher.verify_password(password, user2.password)
        assert user2.login == login
        assert user2.master_password != user1["aes_key"]
