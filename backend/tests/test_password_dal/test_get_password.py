import pytest
from crypting import AES
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
async def test_get_password_by_service_name(
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
    aes = AES(user["aes_key"])
    session = async_session_test()
    async with session.begin():
        password_dal = PasswordDAL(session)
        service_password = await password_dal.get_password_by_service_name(
            user_id=user["user_id"], service_name=service_name
        )
        assert service_password.user_id == user["user_id"]
        assert service_password.service_name == service_name
        assert aes.decrypt_password(service_password.password) == password


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
        ],
        [
            {
                "service_name": "yandex.ru",
                "password": "password1",
            },
            {
                "service_name": "mail.ru",
                "password": "password2",
            },
            {
                "service_name": "google.com",
                "password": "password3",
            },
        ],
    ],
)
async def test_get_all_passwords(
    async_session_test,
    asyncpg_pool,
    passwords_data,
):
    user = await create_user(asyncpg_pool)
    for password_data in passwords_data:
        await create_service_password(
            asyncpg_pool,
            service=password_data["service_name"],
            password=password_data["password"],
            user_id=user["user_id"],
            aes_key=user["aes_key"],
        )
    aes = AES(user["aes_key"])
    session = async_session_test()
    async with session.begin():
        password_dal = PasswordDAL(session)
        service_password = await password_dal.get_all_passwords(user_id=user["user_id"])
        assert len(list(service_password)) == len(passwords_data)
        for db_service_password, parameter_service in zip(
            service_password, passwords_data
        ):
            assert db_service_password.service_name == parameter_service["service_name"]
            assert (
                aes.decrypt_password(db_service_password.password)
                == parameter_service["password"]
            )


@pytest.mark.parametrize(
    "passwords_data, match_service_name, expected_count_data, expected_data",
    [
        (
            [
                {
                    "service_name": "yandex.ru",
                    "password": "password1",
                },
                {
                    "service_name": "mail.ru",
                    "password": "password2",
                },
                {
                    "service_name": "google.com",
                    "password": "password3",
                },
            ],
            ".ru",
            2,
            [
                {
                    "service_name": "yandex.ru",
                    "password": "password1",
                },
                {
                    "service_name": "mail.ru",
                    "password": "password2",
                },
            ],
        ),
        (
            [
                {
                    "service_name": "yandex.ru",
                    "password": "password1",
                },
                {
                    "service_name": "yandex-cloud.ru",
                    "password": "password2",
                },
                {
                    "service_name": "google.com",
                    "password": "password3",
                },
            ],
            "yandex",
            2,
            [
                {
                    "service_name": "yandex.ru",
                    "password": "password1",
                },
                {
                    "service_name": "yandex-cloud.ru",
                    "password": "password2",
                },
            ],
        ),
        (
            [
                {
                    "service_name": "yandex.ru",
                    "password": "password1",
                },
                {
                    "service_name": "yandex-cloud.ru",
                    "password": "password2",
                },
                {
                    "service_name": "google.com",
                    "password": "password3",
                },
            ],
            "mail",
            0,
            [],
        ),
    ],
)
async def test_get_passwords_by_match_service_name(
    async_session_test,
    asyncpg_pool,
    passwords_data,
    match_service_name,
    expected_count_data,
    expected_data,
):
    user = await create_user(asyncpg_pool)
    for password_data in passwords_data:
        await create_service_password(
            asyncpg_pool,
            service=password_data["service_name"],
            password=password_data["password"],
            user_id=user["user_id"],
            aes_key=user["aes_key"],
        )
    aes = AES(user["aes_key"])
    session = async_session_test()
    async with session.begin():
        password_dal = PasswordDAL(session)
        service_password = await password_dal.get_passwords_by_match_service_name(
            user_id=user["user_id"], service_name=match_service_name
        )
        assert len(list(service_password)) == expected_count_data
        for db_service_password, parameter_service in zip(
            service_password, expected_data
        ):
            assert db_service_password.service_name == parameter_service["service_name"]
            assert (
                aes.decrypt_password(db_service_password.password)
                == parameter_service["password"]
            )
