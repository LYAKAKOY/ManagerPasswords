import json
from typing import Callable

import pytest
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
    ],
)
async def test_create_or_update_password_handler(
    client,
    create_user: Callable,
    service_name,
    password_data,
    expected_status_code,
    expected_detail,
):
    user = await create_user()
    response = await client.post(
        f"/passwords/{service_name}",
        content=json.dumps(password_data),
        headers=get_test_auth_headers_for_user(user["user_id"]),
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response == expected_detail
