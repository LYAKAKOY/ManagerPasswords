from api.users.schemas import ChangePasswordUser
from api.users.schemas import CreateUser
from api.users.schemas import ShowUser
from db.users.models import User
from db.users.user_dal import UserDAL
from hashing import Hasher
from sqlalchemy.ext.asyncio import AsyncSession


async def _create_user(body: CreateUser, session: AsyncSession) -> ShowUser | None:
    async with session.begin():
        user_dal = UserDAL(db_session=session)
        user = await user_dal.create_user(
            login=body.login, password=Hasher.get_password_hash(body.password)
        )
        if user is not None:
            return ShowUser(user_id=user.user_id)


async def _change_password_user(
    body: ChangePasswordUser, session: AsyncSession
) -> ShowUser | None:
    async with session.begin():
        user_dal = UserDAL(db_session=session)
        user = await user_dal.set_password(
            login=body.login, password=Hasher.get_password_hash(body.password)
        )
        if user is not None:
            return ShowUser(user_id=user.user_id)


async def _change_master_password_user(
    user: User, session: AsyncSession
) -> ShowUser | None:
    async with session.begin():
        user_dal = UserDAL(db_session=session)
        user = await user_dal.generate_new_master_password(
            user_id=user.user_id, old_aes_key=user.master_password
        )
        if user is not None:
            return ShowUser(user_id=user.user_id)
