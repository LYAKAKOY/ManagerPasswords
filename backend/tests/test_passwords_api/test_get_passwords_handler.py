from typing import Callable

import pytest


@pytest.mark.parametrize(
    "service_name, service_password, service, expected_status_code, expected_detail",
    [
        (
            "yandex.ru",
            "23451",
            "yandex.ru",
            200,
            {"service_name": "yandex.ru", "password": "23451"},
        ),
        (
            "mail.ru",
            "qwerty",
            "mail.ru",
            200,
            {"service_name": "mail.ru", "password": "qwerty"},
        ),
        (
            "mail.ru",
            "qwerty",
            "mail.ry",
            404,
            {"detail": "The password of the service not found"},
        ),
    ],
)
async def test_get_password_by_service_name(
    client,
    create_service_password: Callable,
    create_test_auth_headers_for_user,
    service_name,
    service_password,
    service,
    expected_status_code,
    expected_detail,
):
    await create_service_password(service_name, service_password)
    response = await client.get(
        f"/passwords/{service}", headers=create_test_auth_headers_for_user
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response == expected_detail


@pytest.mark.parametrize(
    "passwords_data, expected_code, expected_data",
    [
        (
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
            200,
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
        ),
        (
            [],
            404,
            {"detail": "Not a single password was found"}
        ),
    ],
)
async def test_get_all_passwords_handler(
    client,
    create_test_auth_headers_for_user,
    create_service_password: Callable,
    passwords_data,
    expected_code,
    expected_data,
):
    for password_data in passwords_data:
        await create_service_password(service=password_data['service_name'],
                                      password=password_data['password'])
    response = await client.get(
        f"/passwords/", headers=create_test_auth_headers_for_user
    )
    data_from_response = response.json()
    assert response.status_code == expected_code
    assert data_from_response == expected_data


@pytest.mark.parametrize(
     "passwords_data, match_service_name, expected_code, expected_data",
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
            200,
            [
                {
                    "service_name": "yandex.ru",
                    "password": "password1",
                },
                {
                    "service_name": "mail.ru",
                    "password": "password2",
                },
            ]
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
            200,
            [
                {
                    "service_name": "yandex.ru",
                    "password": "password1",
                },
                {
                    "service_name": "yandex-cloud.ru",
                    "password": "password2",
                },
            ]
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
            "amazon",
            404,
            {"detail": "No service found"}
        ),
    ],
)
async def test_get_passwords_by_match_service_name_handler(
    client,
    create_test_auth_headers_for_user,
    create_service_password: Callable,
    passwords_data,
    match_service_name,
    expected_code,
    expected_data
):
    for password_data in passwords_data:
        await create_service_password(service=password_data['service_name'],
                                      password=password_data['password'])
    response = await client.get(
        f"/passwords/by_match?match_service_name={match_service_name}",
        headers=create_test_auth_headers_for_user
    )
    data_from_response = response.json()
    assert response.status_code == expected_code
    assert data_from_response == expected_data