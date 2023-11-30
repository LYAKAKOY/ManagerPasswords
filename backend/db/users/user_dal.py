import uuid

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
            if user is not None:
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
