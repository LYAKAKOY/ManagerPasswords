import uuid

from sqlalchemy import update
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
            if password is not None:
                return password
        except IntegrityError:
            await self.db_session.rollback()
            return
