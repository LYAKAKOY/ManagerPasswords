from typing import Callable

import pytest


@pytest.mark.parametrize(
    "service_name, service_password, service, expected_status_code",
    [
        (
            "yandex.ru",
            "23451",
            "yandex.ru",
            200,
        ),
        (
            "mail.ru",
            "qwerty",
            "mail.ru",
            200,
        ),
        (
            "mail.ru",
            "qwerty",
            "mail.ry",
            404,
        ),
    ],
)
async def test_delete_password_by_service_name_handler(
    client,
    create_service_password: Callable,
    create_test_auth_headers_for_user,
    service_name,
    service_password,
    service,
    expected_status_code,
):
    user_id = await create_service_password(service_name, service_password)
    response = await client.delete(
        f"/passwords/{service}", headers=create_test_auth_headers_for_user
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    if expected_status_code == 200:
        assert data_from_response == {"user_id": str(user_id)}
    else:
        assert data_from_response == {"detail": "service not found"}
