import pytest
from crypting import AES
from db.passwords.password_dal import PasswordDAL
from tests.conftest import create_service_password
from tests.conftest import create_user


@pytest.mark.parametrize(
    "service_name, password, new_password",
    [
        (
            "yandex.ru",
            "password1",
            "new_password1",
        ),
        (
            "google.com",
            "password2",
            "new_password2",
        ),
    ],
)
async def test_update_password(
    async_session_test,
    asyncpg_pool,
    service_name,
    password,
    new_password,
):
    user = await create_user(asyncpg_pool)
    await create_service_password(
        asyncpg_pool,
        service=service_name,
        password=password,
        user_id=user["user_id"],
        aes_key=user["aes_key"],
    )
    aes = AES(user["aes_key"])
    session = async_session_test()
    async with session.begin():
        password_dal = PasswordDAL(session)
        service_password = await password_dal.set_password(
            user_id=user["user_id"],
            service_name=service_name,
            password=aes.encrypt_password(new_password),
        )
        assert service_password.user_id == user["user_id"]
        assert service_password.service_name == service_name
        assert aes.decrypt_password(service_password.password) == new_password
