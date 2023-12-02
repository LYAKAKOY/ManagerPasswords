import pytest
from tests.conftest import create_user


@pytest.mark.parametrize(
    "user_data, expected_status_code",
    [
        (
            {
                "login": "login1",
                "password": "ADVCDJ432d",
            },
            200,
        ),
    ],
)
async def test_login_user(
    asyncpg_pool,
    client,
    user_data,
    expected_status_code,
):
    await create_user(
        asyncpg_pool, login=user_data["login"], password=user_data["password"]
    )

    auth_data = {
        "username": user_data["login"],
        "password": user_data["password"],
    }
    response = await client.post(
        "/auth/token",
        data=auth_data,
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response.get("access_token") is not None
    assert data_from_response.get("token_type") == "bearer"


@pytest.mark.parametrize(
    "user_data, expected_status_code, expected_data",
    [
        (
            {
                "login": "login1",
                "password": "ADVCDJ432d",
            },
            401,
            {"detail": "Incorrect username or password"},
        ),
    ],
)
async def test_login_user_incorrect_login(
    asyncpg_pool, client, user_data, expected_status_code, expected_data
):
    await create_user(
        asyncpg_pool, login=user_data["login"], password=user_data["password"]
    )

    auth_data = {
        "username": user_data["login"] + "1",
        "password": user_data["password"],
    }
    response = await client.post(
        "/auth/token",
        data=auth_data,
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response == expected_data


@pytest.mark.parametrize(
    "user_data, expected_status_code, expected_data",
    [
        (
            {
                "login": "login1",
                "password": "ADVCDJ432d",
            },
            401,
            {"detail": "Incorrect username or password"},
        ),
    ],
)
async def test_login_user_incorrect_password(
    asyncpg_pool, client, user_data, expected_status_code, expected_data
):
    await create_user(
        asyncpg_pool, login=user_data["login"], password=user_data["password"]
    )

    auth_data = {
        "username": user_data["login"],
        "password": user_data["password"] + "1",
    }
    response = await client.post(
        "/auth/token",
        data=auth_data,
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response == expected_data


async def test_login_without_username_and_password(client):

    auth_data = {}
    response = await client.post(
        "/auth/token",
        data=auth_data,
    )
    data_from_response = response.json()
    assert response.status_code == 422
    assert data_from_response == {
        "detail": [
            {
                "input": None,
                "loc": ["body", "username"],
                "msg": "Field required",
                "type": "missing",
                "url": "https://errors.pydantic.dev/2.5/v/missing",
            },
            {
                "input": None,
                "loc": ["body", "password"],
                "msg": "Field required",
                "type": "missing",
                "url": "https://errors.pydantic.dev/2.5/v/missing",
            },
        ]
    }
