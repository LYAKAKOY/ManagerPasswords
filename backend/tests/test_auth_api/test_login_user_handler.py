import pytest

from db.users.user_dal import UserDAL
from hashing import Hasher


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
    ]
)
async def test_login_user(
        async_session_test,
        client,
        user_data,
        expected_status_code,
):
    session = async_session_test()
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(login="login1", password=Hasher.get_password_hash("ADVCDJ432d"))

    auth_data = {
        "username": user.login,
        "password": "ADVCDJ432d",
    }
    response = await client.post("/login/token",
                                 data=auth_data,
                                 )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response.get('access_token') is not None
    assert data_from_response.get('token_type') == "bearer"

@pytest.mark.parametrize(
    "user_data, expected_status_code, expected_data",
    [
        (
                {
                    "login": "login1",
                    "password": "ADVCDJ432d",
                },
                401,
                {
                    "detail": "Incorrect username or password"
                }
        ),
    ]
)
async def test_login_user_incorrect_login(
        async_session_test,
        client,
        user_data,
        expected_status_code,
        expected_data
):
    session = async_session_test()
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(login="login1", password=Hasher.get_password_hash("ADVCDJ432d"))

    auth_data = {
        "username": user.login + '1',
        "password": "ADVCDJ432d",
    }
    response = await client.post("/login/token",
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
                {
                    "detail": "Incorrect username or password"
                }
        ),
    ]
)
async def test_login_user_incorrect_password(
        async_session_test,
        client,
        user_data,
        expected_status_code,
        expected_data
):
    session = async_session_test()
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(login="login1", password=Hasher.get_password_hash("ADVCDJ432d"))

    auth_data = {
        "username": user.login,
        "password": "ADVCDJ432d2",
    }
    response = await client.post("/login/token",
                                 data=auth_data,
                                 )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response == expected_data