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
        except IntegrityError:
            await self.db_session.rollback()
            return