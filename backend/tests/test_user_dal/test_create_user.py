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
    login,
    password
):
    session = async_session()
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(login=login, password=password)
        assert user.login == login
        assert user.password == password
