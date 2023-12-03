import pytest
from tests.conftest import create_service_password
from tests.conftest import create_user
from tests.conftest import get_test_auth_headers_for_user


@pytest.mark.parametrize(
    "user_data, passwords_data, expected_status_code",
    [
        (
            {
                "login": "login1",
                "password": "test_password1",
            },
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
            200,
        ),
    ],
)
async def test_change_master_password_user(
    client,
    asyncpg_pool,
    user_data,
    passwords_data,
    expected_status_code,
):
    user = await create_user(
        asyncpg_pool, login=user_data["login"], password=user_data["password"]
    )
    for password_data in passwords_data:
        await create_service_password(
            asyncpg_pool,
            service=password_data["service_name"],
            password=password_data["password"],
            user_id=user["user_id"],
            aes_key=user["aes_key"],
        )
    response = await client.put(
        "/user/change_master_password",
        headers=get_test_auth_headers_for_user(user["user_id"]),
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response.get("user_id") == str(user["user_id"])
    response = await client.get(
        "/passwords/", headers=get_test_auth_headers_for_user(user["user_id"])
    )
    data_from_response = response.json()
    assert response.status_code == 200
    assert data_from_response == passwords_data
