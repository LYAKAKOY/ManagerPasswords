from db.users.user_dal import UserDAL
import pytest

from tests.db_test import async_session


@pytest.mark.parametrize(
    "login, password",
    [
        (
           "login1",
           "password1"

        ),
        (
           "login2",
           "password2"

        ),
    ],
)
async def test_create_user(
    async_session_test,
    login,
    password
):
    session = async_session_test()
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(login=login, password=password)
        assert user.login == login
        assert user.password == password

async def test_create_user_duplicate_login(async_session_test):
    session = async_session_test()
    for _ in range(2):
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(login="login", password="12345")
    assert user is None
