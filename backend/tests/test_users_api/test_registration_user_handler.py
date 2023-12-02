import json

import pytest
from tests.conftest import create_user


@pytest.mark.parametrize(
    "user_data, expected_status_code",
    [
        (
            {
                "login": "login1",
                "password": "test_password1",
            },
            200,
        ),
        (
            {
                "login": "login2",
                "password": "test_password2",
            },
            200,
        ),
    ],
)
async def test_create_user_handler(
    client,
    user_data,
    expected_status_code,
):
    response = await client.post(
        "/user/reg",
        content=json.dumps(user_data),
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response.get("user_id") is not None


@pytest.mark.parametrize(
    "user_data, expected_status_code, expected_data",
    [
        (
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
                "password": "qwerty",
            },
            422,
            {"detail": "the password is too simple"},
        ),
    ],
)
async def test_create_user_with_simple_password(
    client,
    user_data,
    expected_status_code,
    expected_data,
):
    response = await client.post(
        "/user/reg",
        content=json.dumps(user_data),
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response == expected_data


@pytest.mark.parametrize(
    "user_data, expected_status_code, expected_data",
    [
        (
            {
                "login": "log1",
                "password": "ADVCDJ432d",
            },
            422,
            {"detail": "the login is too short"},
        ),
        (
            {
                "login": "log2",
                "password": "ASDFVy13",
            },
            422,
            {"detail": "the login is too short"},
        ),
    ],
)
async def test_create_user_with_short_login(
    client,
    user_data,
    expected_status_code,
    expected_data,
):
    response = await client.post(
        "/user/reg",
        content=json.dumps(user_data),
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response == expected_data


async def test_create_user_with_exists_login(
    client,
    asyncpg_pool,
):
    user_data = {
        "login": "login1",
        "password": "test_password1",
    }
    await create_user(
        asyncpg_pool, login=user_data["login"], password=user_data["password"]
    )
    response = await client.post(
        "/user/reg",
        content=json.dumps(user_data),
    )
    data_from_response = response.json()
    assert response.status_code == 422
    assert data_from_response == {"detail": "this login is already exists"}


async def test_create_user_without_data(
    client,
):
    user_data = {}
    response = await client.post(
        "/user/reg",
        content=json.dumps(user_data),
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
