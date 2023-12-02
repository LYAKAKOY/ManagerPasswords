import pytest
from tests.conftest import create_service_password
from tests.conftest import create_user
from tests.conftest import get_test_auth_headers_for_user


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
async def test_get_password_by_service_name_handler(
    client,
    asyncpg_pool,
    service_name,
    service_password,
    service,
    expected_status_code,
    expected_detail,
):
    user = await create_user(asyncpg_pool)
    await create_service_password(
        asyncpg_pool,
        service=service_name,
        password=service_password,
        user_id=user["user_id"],
        aes_key=user["aes_key"],
    )
    response = await client.get(
        f"/passwords/{service}", headers=get_test_auth_headers_for_user(user["user_id"])
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
                },
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
                },
            ],
        ),
        ([], 404, {"detail": "Not a single password was found"}),
    ],
)
async def test_get_all_passwords_handler(
    client,
    asyncpg_pool,
    passwords_data,
    expected_code,
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
    response = await client.get(
        "/passwords/", headers=get_test_auth_headers_for_user(user["user_id"])
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
            "amazon",
            404,
            {"detail": "No service found"},
        ),
    ],
)
async def test_get_passwords_by_match_service_name_handler(
    client,
    asyncpg_pool,
    passwords_data,
    match_service_name,
    expected_code,
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
    response = await client.get(
        f"/passwords/by_match?match_service_name={match_service_name}",
        headers=get_test_auth_headers_for_user(user["user_id"]),
    )
    data_from_response = response.json()
    assert response.status_code == expected_code
    assert data_from_response == expected_data
