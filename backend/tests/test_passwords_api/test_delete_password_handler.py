import pytest
from tests.conftest import create_service_password
from tests.conftest import create_user
from tests.conftest import get_test_auth_headers_for_user


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
    asyncpg_pool,
    service_name,
    service_password,
    service,
    expected_status_code,
):
    user = await create_user(asyncpg_pool)
    await create_service_password(
        asyncpg_pool,
        service=service_name,
        password=service_password,
        user_id=user["user_id"],
        aes_key=user["aes_key"],
    )
    response = await client.delete(
        f"/passwords/{service}", headers=get_test_auth_headers_for_user(user["user_id"])
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    if expected_status_code == 200:
        assert data_from_response == {"user_id": str(user["user_id"])}
    else:
        assert data_from_response == {"detail": "service not found"}
