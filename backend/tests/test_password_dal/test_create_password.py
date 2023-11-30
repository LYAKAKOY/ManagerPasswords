import pytest
from crypting import AES
from db.passwords.password_dal import PasswordDAL


@pytest.mark.parametrize(
    "service_name, password",
    [
        ("yandex.ru", "password1"),
        ("google.com", "password2"),
    ],
)
async def test_create_password(async_session_test, create_user, service_name, password):
    session = async_session_test()
    async with session.begin():
        password_dal = PasswordDAL(session)
        service_password = await password_dal.create_password(
            user_id=create_user,
            service_name=service_name,
            password=AES.encrypt_password(password),
        )
        assert service_password.user_id == create_user
        assert service_password.service_name == service_name
        assert AES.decrypt_password(service_password.password) == password
