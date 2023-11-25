from sqlalchemy.ext.asyncio import AsyncSession

from api.users.schemas import CreateUser, ShowUser
from db.users.user_dal import UserDAL
from hashing import Hasher


async def _create_user(body: CreateUser, session: AsyncSession) -> ShowUser | None:
    async with session.begin():
        user_dal = UserDAL(db_session=session)
        user = await user_dal.create_user(login=body.login, password=Hasher.get_password_hash(body.password))
        if user is not None:
            return ShowUser(user_id=user.user_id)