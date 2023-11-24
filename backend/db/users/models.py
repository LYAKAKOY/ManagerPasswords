import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapper, mapped_column

from db.base import Base


class User(Base):

    user_id: Mapper[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4(), server_default=str(uuid.uuid4()))
    login: Mapper[str] = mapped_column(String(15), unique=True, index=True)
    password: Mapper[str]
