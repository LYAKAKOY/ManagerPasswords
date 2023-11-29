from typing import Callable

from crypting import AES
from db.passwords.password_dal import PasswordDAL
import pytest


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
async def test_get_password_by_service_name(
    async_session_test,
    create_service_password: Callable,
    service_name,
    password,
):
    user_id = await create_service_password(service=service_name, password=password)
    session = async_session_test()
    async with session.begin():
        password_dal = PasswordDAL(session)
        service_password = await password_dal.get_password(user_id=user_id, service_name=service_name)
        assert service_password.user_id == user_id
        assert service_password.service_name == service_name
        assert AES.decrypt_password(service_password.password) == password

@pytest.mark.parametrize(
    "password_data1, password_data2",
    [
        (
            {
                "service_name": "yandex.ru",
                "password": "password1",
            } ,
            {
                "service_name": "google.com",
                "password": "password2",
            }
        )
    ],
)
async def test_get_all_password(
    async_session_test,
    create_service_password: Callable,
    password_data1,
    password_data2,
):

    await create_service_password(service=password_data1['service_name'],
                                            password=password_data1['password'])
    user_id = await create_service_password(service=password_data2['service_name'],
                                            password=password_data2['password'])
    session = async_session_test()
    async with session.begin():
        password_dal = PasswordDAL(session)
        service_password = await password_dal.get_all_passwords(user_id=user_id)
        assert len(list(service_password)) == 2
        for db_service_password, parameter_service in zip(service_password, [password_data1, password_data2]):
            assert db_service_password.service_name == parameter_service['service_name']
            assert AES.decrypt_password(db_service_password.password) == parameter_service['password']