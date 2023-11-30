from typing import Callable

import pytest


@pytest.mark.parametrize(
    "service_name, service_password, expected_status_code, expected_detail",
    [
        (
            "yandex.ru",
            "23451",
            200,
            {"service_name": "yandex.ru", "password": "23451"},
        ),
        (
            "mail.ru",
            "qwerty",
            200,
            {"service_name": "mail.ru", "password": "qwerty"},
        ),
    ],
)
async def test_get_password_by_service_name(
    client,
    create_service_password: Callable,
    create_test_auth_headers_for_user,
    service_name,
    service_password,
    expected_status_code,
    expected_detail,
):
    await create_service_password(service_name, service_password)
    response = await client.get(
        f"/passwords/{service_name}", headers=create_test_auth_headers_for_user
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response == expected_detail


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
            }
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
    client,
    create_test_auth_headers_for_user,
    create_service_password: Callable,
    passwords_data,
):
    for password_data in passwords_data:
        await create_service_password(service=password_data['service_name'],
                                      password=password_data['password'])
    response = await client.get(
        f"/passwords/", headers=create_test_auth_headers_for_user
    )
    data_from_response = response.json()
    assert response.status_code == 200
    assert data_from_response == passwords_data