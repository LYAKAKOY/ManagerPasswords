from typing import Callable

import pytest
from db.passwords.password_dal import PasswordDAL


@pytest.mark.parametrize(
    "service_name, password",
    [
        (
            "yandex.ru",
            "password1",
        ),
        (
            "google.com",
            "password2",
        ),
    ],
)
async def test_update_password(
    async_session_test,
    create_user: Callable,
    create_service_password: Callable,
    service_name,
    password,
):
    user = await create_user()
    await create_service_password(
        service=service_name,
        password=password,
        user_id=user["user_id"],
        aes_key=user["aes_key"],
    )
    session = async_session_test()
    async with session.begin():
        password_dal = PasswordDAL(session)
        deleted_password_user_id = await password_dal.delete_password_by_service_name(
            user_id=user["user_id"], service_name=service_name
        )
        assert deleted_password_user_id == user["user_id"]
