import pytest
from db.users.user_dal import UserDAL


@pytest.mark.parametrize(
    "login, password",
    [
        ("login1", "password1"),
    ],
)
async def test_get_user_by_user_id(async_session_test, login, password):
    session = async_session_test()
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(login=login, password=password)
    async with session.begin():
        user_dal = UserDAL(session)
        got_user = await user_dal.get_user_by_user_id(user_id=user.user_id)
    assert user == got_user


@pytest.mark.parametrize(
    "login, password",
    [
        ("login1", "password1"),
    ],
)
async def test_get_user_by_login(async_session_test, login, password):
    session = async_session_test()
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(login=login, password=password)
    async with session.begin():
        user_dal = UserDAL(session)
        got_user = await user_dal.get_user_by_login(login=user.login)
    assert user == got_user
