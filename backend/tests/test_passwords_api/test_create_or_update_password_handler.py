import json

import pytest
from tests.conftest import create_user
from tests.conftest import get_test_auth_headers_for_user


@pytest.mark.parametrize(
    "service_name, password_data, expected_status_code, expected_detail",
    [
        (
            "yandex.ru",
            {
                "password": "12345",
            },
            200,
            {"service_name": "yandex.ru", "password": "12345"},
        ),
        (
            "yandex.ru",
            {
                "password": "23451",
            },
            200,
            {"service_name": "yandex.ru", "password": "23451"},
        ),
        (
            "mail.ru",
            {
                "password": "qwerty",
            },
            200,
            {"service_name": "mail.ru", "password": "qwerty"},
        ),
        (
            "yandex.ru",
            {},
            422,
            {
                "detail": [
                    {
                        "input": {},
                        "loc": ["body", "password"],
                        "msg": "Field required",
                        "type": "missing",
                        "url": "https://errors.pydantic.dev/2.5/v/missing",
                    }
                ]
            },
        ),
    ],
)
async def test_create_or_update_password_handler(
    client,
    asyncpg_pool,
    service_name,
    password_data,
    expected_status_code,
    expected_detail,
):
    user = await create_user(asyncpg_pool)
    response = await client.post(
        f"/passwords/{service_name}",
        content=json.dumps(password_data),
        headers=get_test_auth_headers_for_user(user["user_id"]),
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response == expected_detail


async def test_create_or_update_password_handler_without_headers(
    client,
    asyncpg_pool,
):
    service_name = "yandex.ru"
    password_data = {
        "password": "23451",
    }
    await create_user(asyncpg_pool)
    response = await client.post(
        f"/passwords/{service_name}",
        content=json.dumps(password_data),
    )
    data_from_response = response.json()
    assert response.status_code == 401
    assert data_from_response == {"detail": "Not authenticated"}
