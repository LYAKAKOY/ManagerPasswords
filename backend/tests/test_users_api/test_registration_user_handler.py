import json
import pytest

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
    ]
)
async def test_create_user_handler(
    client,
    user_data,
    expected_status_code,
):
    response = await client.post("/user/reg",
        data=json.dumps(user_data),
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response.get('user_id') is not None