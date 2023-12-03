import uuid
from typing import List

from crypting import AES
from db.passwords.models import Password
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class PasswordDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_password(
        self, user_id: uuid.UUID, service_name: str, password: bytes
    ) -> Password | None:
        new_password = Password(
            user_id=user_id, service_name=service_name, password=password
        )
        try:
            self.db_session.add(new_password)
            await self.db_session.flush()
            await self.db_session.commit()
            return new_password
        except IntegrityError:
            await self.db_session.rollback()
            return

    async def set_password(
        self, user_id: uuid.UUID, service_name: str, password: bytes
    ) -> Password | None:
        query = (
            update(Password)
            .where(Password.user_id == user_id, Password.service_name == service_name)
            .values(password=password)
            .returning(Password)
        )
        try:
            password = await self.db_session.scalar(query)
            await self.db_session.commit()
            if password is not None:
                return password
        except IntegrityError:
            await self.db_session.rollback()
            return

    async def change_aes_key(
        self, user_id: uuid.UUID, old_aes_key: bytes, new_aes_key: bytes
    ) -> List[Password] | None:
        service_passwords = await self.get_all_passwords(user_id=user_id)
        if service_passwords is None:
            return
        aes = AES(old_aes_key)
        service_passwords = [
            Password(
                service_name=service.service_name,
                password=aes.decrypt_password(service.password),
                user_id=service.user_id,
            )
            for service in service_passwords
        ]
        for service_password in service_passwords:
            query = (
                delete(Password)
                .where(
                    Password.user_id == user_id,
                    Password.service_name == service_password.service_name,
                )
                .returning(Password.user_id)
            )
            await self.db_session.execute(query)
        aes = AES(new_aes_key)
        new_passwords = []
        service_passwords = [
            Password(
                service_name=service.service_name,
                password=aes.encrypt_password(service.password),
                user_id=service.user_id,
            )
            for service in service_passwords
        ]
        for service in service_passwords:
            self.db_session.add(service)
            await self.db_session.flush()
            new_passwords.append(service)
        return new_passwords

    async def delete_password_by_service_name(
        self, user_id: uuid.UUID, service_name: str
    ) -> int | None:
        query = (
            delete(Password)
            .where(Password.user_id == user_id, Password.service_name == service_name)
            .returning(Password.user_id)
        )
        try:
            user_id = await self.db_session.scalar(query)
            await self.db_session.commit()
            if user_id is not None:
                return user_id
        except IntegrityError:
            await self.db_session.rollback()
            return

    async def get_password_by_service_name(
        self, user_id: uuid.UUID, service_name: str
    ) -> Password | None:
        query = select(Password).where(
            Password.user_id == user_id, Password.service_name == service_name
        )
        password = await self.db_session.scalar(query)
        if password is not None:
            return password

    async def get_passwords_by_match_service_name(
        self, user_id: uuid.UUID, service_name: str
    ) -> List[Password] | None:
        query = (
            select(Password)
            .where(Password.user_id == user_id)
            .filter(Password.service_name.contains(service_name))
        )
        passwords = await self.db_session.scalars(query)
        if passwords is not None:
            return passwords

    async def get_all_passwords(self, user_id: uuid.UUID) -> List[Password] | None:
        query = select(Password).where(Password.user_id == user_id)
        passwords = await self.db_session.scalars(query)
        if passwords is not None:
            return passwords
