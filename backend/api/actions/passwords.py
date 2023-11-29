from typing import List

from crypting import AES
from api.passwords.schemas import CreatePassword
from api.passwords.schemas import ShowPassword
from db.passwords.password_dal import PasswordDAL
from db.users.models import User
from sqlalchemy.ext.asyncio import AsyncSession


async def _create_or_update_password(
    service_name: str, body: CreatePassword, current_user: User, session: AsyncSession
) -> ShowPassword | None:
    async with session.begin():
        password_dal = PasswordDAL(session)
        if await password_dal.get_password_by_service_name(user_id=current_user.user_id,
                                                                   service_name=service_name):
            service_password = await password_dal.set_password(
                user_id=current_user.user_id,
                service_name=service_name,
                password=AES.encrypt_password(body.password),
            )

        else:
            service_password = await password_dal.create_password(
                service_name=service_name,
                user_id=current_user.user_id,
                password=AES.encrypt_password(body.password),
            )
        if service_password is not None:
            return ShowPassword(service_name=service_password.service_name,
                                password=AES.decrypt_password(service_password.password))

async def _get_password_by_service_name(
    service_name: str, current_user: User, session: AsyncSession
) -> ShowPassword | None:
    async with session.begin():
        password_dal = PasswordDAL(session)
        service_password = await password_dal.get_password_by_service_name(
            user_id=current_user.user_id, service_name=service_name
        )
        if service_password is not None:
            return ShowPassword(
                service_name=service_password.service_name,
                password=AES.decrypt_password(service_password.password),
            )

async def _get_passwords_by_match_service_name(
    service_name: str, current_user: User, session: AsyncSession
) -> List[ShowPassword] | None:
    async with session.begin():
        password_dal = PasswordDAL(session)
        passwords = await password_dal.get_passwords_by_match_service_name(
            user_id=current_user.user_id, service_name=service_name
        )
        if passwords is not None:
            all_show_passwords = []
            for password in passwords:
                all_show_passwords.append(
                    ShowPassword(
                        service_name=password.service_name,
                        password=AES.decrypt_password(password.password),
                    )
                )
            return all_show_passwords