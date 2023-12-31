import uuid

from cryptography.fernet import Fernet
from db.passwords.password_dal import PasswordDAL
from db.users.models import User
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, login: str, password: str) -> User | None:
        new_user = User(login=login, password=password)
        try:
            self.db_session.add(new_user)
            await self.db_session.flush()
            await self.db_session.commit()
            return new_user
        except IntegrityError:
            await self.db_session.rollback()
            return

    async def set_password(self, login: str, password: str) -> User | None:
        try:
            query = (
                update(User)
                .where(User.login == login)
                .values(password=password)
                .returning(User)
            )
            user = await self.db_session.scalar(query)
            await self.db_session.commit()
            if user is not None:
                return user
        except IntegrityError:
            await self.db_session.rollback()
            return

    async def generate_new_master_password(
        self, user_id: uuid.UUID, old_aes_key: bytes
    ) -> User:
        try:
            query = (
                update(User)
                .where(User.user_id == user_id)
                .values(master_password=Fernet.generate_key())
                .returning(User)
            )
            user = await self.db_session.scalar(query)
            if user is not None:
                password_dal = PasswordDAL(self.db_session)
                await password_dal.change_aes_key(
                    user_id=user_id,
                    old_aes_key=old_aes_key,
                    new_aes_key=user.master_password,
                )
                await self.db_session.commit()
                return user
        except IntegrityError:
            await self.db_session.rollback()
            return

    async def get_user_by_login(self, login: str) -> User | None:
        query = select(User).where(User.login == login)
        user = await self.db_session.scalar(query)
        if user is not None:
            return user

    async def get_user_by_user_id(self, user_id: uuid.UUID) -> User | None:
        user = await self.db_session.get(User, user_id)
        if user is not None:
            return user
