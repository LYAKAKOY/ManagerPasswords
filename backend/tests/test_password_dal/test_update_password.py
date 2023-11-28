from crypting import AES
from db.passwords.password_dal import PasswordDAL
import pytest


@pytest.mark.parametrize(
    "service_name, password, new_password",
    [
        (
           "yandex.ru",
           "password1",
           "new_password1",

        ),
        (
           "google.com",
           "password2",
           "new_password2",

        ),
    ],
)
async def test_update_password(
    async_session_test,
    create_service_password,
    service_name,
    password,
    new_password
):
    user_id = await create_service_password(service=service_name, password=password)
    session = async_session_test()
    async with session.begin():
        password_dal = PasswordDAL(session)
        service_password = await password_dal.set_password(user_id=user_id, service_name=service_name,
                                                              password=AES.encrypt_password(new_password))
        assert service_password.user_id == user_id
        assert service_password.service_name == service_name
        assert AES.decrypt_password(service_password.password) == new_password