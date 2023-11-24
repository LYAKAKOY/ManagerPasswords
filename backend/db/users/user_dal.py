from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.users.models import User


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
            query = update(User).where(User.login == login).values(password=password).returning(User.user_id)
            user = await self.db_session.scalar(query)
            if user is None:
                return user
        except IntegrityError:
            await self.db_session.rollback()
            return

