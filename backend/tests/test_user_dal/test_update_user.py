import pytest
from db.users.user_dal import UserDAL


@pytest.mark.parametrize(
    "login, password, new_password",
    [
        ("login1", "password1", "new_password1"),
    ],
)
async def test_update_user_password(async_session_test, login, password, new_password):
    session = async_session_test()
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(login=login, password=password)
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.set_password(login=login, password=new_password)
        assert user.password == new_password
