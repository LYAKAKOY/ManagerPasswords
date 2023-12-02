import pytest
from crypting import AES
from cryptography.fernet import Fernet
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


@pytest.mark.parametrize(
    "passwords_data",
    [
        [
            {
                "service_name": "yandex.ru",
                "password": "password1",
            },
            {
                "service_name": "google.com",
                "password": "password2",
            },
            {
                "service_name": "amazon.com",
                "password": "password3",
            },
        ],
    ],
)
async def test_update_aes_key(
    async_session_test,
    asyncpg_pool,
    passwords_data,
):
    user = await create_user(asyncpg_pool)
    for password in passwords_data:
        await create_service_password(
            asyncpg_pool,
            service=password["service_name"],
            password=password["password"],
            user_id=user["user_id"],
            aes_key=user["aes_key"],
        )
    aes = AES(user["aes_key"])
    session = async_session_test()
    async with session.begin():
        password_dal = PasswordDAL(session)
        new_aes_key = Fernet.generate_key()
        service_passwords = await password_dal.change_aes_key(
            user_id=user["user_id"],
            old_aes_key=user["aes_key"],
            new_aes_key=new_aes_key,
        )
        aes = AES(new_aes_key)
        for new_password, password_data in zip(service_passwords, passwords_data):
            assert new_password.user_id == user["user_id"]
            assert new_password.service_name == password_data["service_name"]
            assert (
                aes.decrypt_password(new_password.password) == password_data["password"]
            )
