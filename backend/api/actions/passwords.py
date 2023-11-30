from typing import List

from crypting import AES
from api.passwords.schemas import CreatePassword, DeletedPassword
from api.passwords.schemas import ShowPassword
from db.passwords.password_dal import PasswordDAL
from db.users.models import User
from sqlalchemy.ext.asyncio import AsyncSession


async def _create_or_update_password(
    service_name: str, body: CreatePassword, user: User, session: AsyncSession
) -> ShowPassword | None:
    async with session.begin():
        password_dal = PasswordDAL(session)
        if await password_dal.get_password_by_service_name(user_id=user.user_id,
                                                                   service_name=service_name):
            service_password = await password_dal.set_password(
                user_id=user.user_id,
                service_name=service_name,
                password=AES.encrypt_password(body.password),
            )

        else:
            service_password = await password_dal.create_password(
                service_name=service_name,
                user_id=user.user_id,
                password=AES.encrypt_password(body.password),
            )
        if service_password is not None:
            return ShowPassword(service_name=service_password.service_name,
                                password=AES.decrypt_password(service_password.password))

async def _get_password_by_service_name(
    service_name: str, user: User, session: AsyncSession
) -> ShowPassword | None:
    async with session.begin():
        password_dal = PasswordDAL(session)
        service_password = await password_dal.get_password_by_service_name(
            user_id=user.user_id, service_name=service_name
        )
        if service_password is not None:
            return ShowPassword(
                service_name=service_password.service_name,
                password=AES.decrypt_password(service_password.password),
            )

async def _get_passwords_by_match_service_name(
    service_name: str, user: User, session: AsyncSession
) -> List[ShowPassword] | None:
    async with session.begin():
        password_dal = PasswordDAL(session)
        service_passwords = await password_dal.get_passwords_by_match_service_name(
            user_id=user.user_id, service_name=service_name
        )
        if service_passwords is not None:
            all_show_passwords = []
            for service_password in service_passwords:
                all_show_passwords.append(
                    ShowPassword(
                        service_name=service_password.service_name,
                        password=AES.decrypt_password(service_password.password),
                    )
                )
            return all_show_passwords

async def _get_all_passwords(
    user: User, session: AsyncSession
) -> List[ShowPassword] | None:
    async with session.begin():
        password_dal = PasswordDAL(session)
        service_passwords = await password_dal.get_all_passwords(user_id=user.user_id)
        if service_passwords is not None:
            all_show_passwords = []
            for service_password in service_passwords:
                all_show_passwords.append(
                    ShowPassword(
                        service_name=service_password.service_name,
                        password=AES.decrypt_password(service_password.password),
                    )
                )
            return all_show_passwords

async def _delete_password_by_service_name(service_name: str, user: User, session: AsyncSession) -> DeletedPassword | None:
    async with session.begin():
        password_dal = PasswordDAL(session)
        password_id = await password_dal.delete_password_by_service_name(user_id=user.user_id, service_name=service_name)
        if password_id is not None:
            return DeletedPassword(password_id=password_id)