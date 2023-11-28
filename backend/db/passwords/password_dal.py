import uuid
from typing import List

from sqlalchemy import update, delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.passwords.models import Password, HexByteString


class PasswordDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_password(self, user_id: uuid.UUID, service_name: str, password: HexByteString) -> Password | None:
        new_password = Password(user_id=user_id, service_name=service_name, password=password)
        try:
            self.db_session.add(new_password)
            await self.db_session.flush()
            await self.db_session.commit()
            return new_password
        except IntegrityError:
            await self.db_session.rollback()
            return

    async def set_password(self, user_id: uuid.UUID, service_name: str, password: HexByteString) -> Password | None:
        query = update(Password).where(Password.user_id == user_id, Password.service_name == service_name).\
            values(password=password).returning(Password)
        try:
            password = await self.db_session.scalar(query)
            await self.db_session.commit()
            if password is not None:
                return password
        except IntegrityError:
            await self.db_session.rollback()
            return

    async def delete_password(self, user_id: uuid.UUID, service_name: str) -> int | None:
        query = delete(Password).where(Password.user_id == user_id, Password.service_name == service_name).\
            returning(Password.user_id)
        try:
            password_id = await self.db_session.scalar(query)
            await self.db_session.commit()
            if password_id is not None:
                return password_id
        except IntegrityError:
            await self.db_session.rollback()
            return
    async def get_password(self, user_id: uuid.UUID, service_name: str) -> Password | None:
        query = (
            select(Password)
            .where(Password.user_id == user_id, Password.service_name == service_name)
        )
        password = await self.db_session.scalars(query)
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
        query = (
            select(Password)
            .where(Password.user_id == user_id)
        )
        passwords = await self.db_session.scalars(query)
        if passwords is not None:
            return passwords