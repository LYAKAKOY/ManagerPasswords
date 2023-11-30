import json

import pytest


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
    create_test_auth_headers_for_user,
    service_name,
    password_data,
    expected_status_code,
    expected_detail,
):
    response = await client.post(
        f"/passwords/{service_name}",
        content=json.dumps(password_data),
        headers=create_test_auth_headers_for_user,
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response == expected_detail