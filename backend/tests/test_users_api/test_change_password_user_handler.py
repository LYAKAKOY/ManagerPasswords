import json

import pytest


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
    user_data,
    new_user_data,
    expected_status_code,
):
    await client.post(
        "/user/reg",
        content=json.dumps(user_data),
    )
    response = await client.put(
        "/user/change_password",
        content=json.dumps(new_user_data),
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response.get("user_id") is not None


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
    user_data,
    new_user_data,
    expected_status_code,
    expected_data,
):
    await client.post(
        "/user/reg",
        content=json.dumps(user_data),
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
