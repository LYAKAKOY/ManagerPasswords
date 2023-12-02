import pytest
from db.passwords.password_dal import PasswordDAL
from tests.conftest import create_service_password
from tests.conftest import create_user


@pytest.mark.parametrize(
    "service_name, password",
    [
        (
            "yandex.ru",
            "password1",
        ),
        (
            "google.com",
            "password2",
        ),
    ],
)
async def test_delete_password(
    async_session_test,
    asyncpg_pool,
    service_name,
    password,
):
    user = await create_user(asyncpg_pool)
    await create_service_password(
        asyncpg_pool,
        service=service_name,
        password=password,
        user_id=user["user_id"],
        aes_key=user["aes_key"],
    )
    session = async_session_test()
    async with session.begin():
        password_dal = PasswordDAL(session)
        deleted_password_user_id = await password_dal.delete_password_by_service_name(
            user_id=user["user_id"], service_name=service_name
        )
        assert deleted_password_user_id == user["user_id"]
