import json

import pytest
from tests.conftest import create_user


@pytest.mark.parametrize(
    "user_data, new_user_data, expected_status_code",
    [
        (
            {
                "login": "login1",
                "password": "test_password1",
            },
            {
                "login": "login1",
                "password": "new_test_password1",
            },
            200,
        ),
        (
            {
                "login": "login2",
                "password": "test_password2",
            },
            {
                "login": "login2",
                "password": "new_test_password2",
            },
            200,
        ),
    ],
)
async def test_change_password_user(
    client,
    asyncpg_pool,
    user_data,
    new_user_data,
    expected_status_code,
):
    user = await create_user(
        asyncpg_pool, login=user_data["login"], password=user_data["password"]
    )
    response = await client.put(
        "/user/change_password",
        content=json.dumps(new_user_data),
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response.get("user_id") == str(user["user_id"])


@pytest.mark.parametrize(
    "user_data, new_user_data, expected_status_code, expected_data",
    [
        (
            {
                "login": "login1",
                "password": "test_password1",
            },
            {
                "login": "login1",
                "password": "12345",
            },
            422,
            {"detail": "the password is too simple"},
        ),
        (
            {
                "login": "login2",
                "password": "test_password2",
            },
            {
                "login": "login2",
                "password": "qwerty",
            },
            422,
            {"detail": "the password is too simple"},
        ),
    ],
)
async def test_change_password_user_with_simple_password(
    client,
    asyncpg_pool,
    user_data,
    new_user_data,
    expected_status_code,
    expected_data,
):
    await create_user(
        asyncpg_pool, login=user_data["login"], password=user_data["password"]
    )
    response = await client.put(
        "/user/change_password",
        content=json.dumps(new_user_data),
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response == expected_data


@pytest.mark.parametrize(
    "new_user_data, expected_status_code, expected_data",
    [
        (
            {
                "login": "login1",
                "password": "new_est_password1",
            },
            404,
            {"detail": "User not found"},
        ),
    ],
)
async def test_change_password_non_existent_user(
    client,
    new_user_data,
    expected_status_code,
    expected_data,
):
    response = await client.put(
        "/user/change_password",
        content=json.dumps(new_user_data),
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response == expected_data


async def test_change_password_without_data(
    client,
):
    new_user_data = {}
    response = await client.put(
        "/user/change_password",
        content=json.dumps(new_user_data),
    )
    data_from_response = response.json()
    assert response.status_code == 422
    assert data_from_response == {
        "detail": [
            {
                "input": {},
                "loc": ["body", "login"],
                "msg": "Field required",
                "type": "missing",
                "url": "https://errors.pydantic.dev/2.5/v/missing",
            },
            {
                "input": {},
                "loc": ["body", "password"],
                "msg": "Field required",
                "type": "missing",
                "url": "https://errors.pydantic.dev/2.5/v/missing",
            },
        ]
    }
