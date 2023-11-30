import uuid
from typing import List

from db.base import Base
from db.passwords.models import Password
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class User(Base):

    user_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4(), server_default=str(uuid.uuid4())
    )
    login: Mapped[str] = mapped_column(String(15), unique=True, index=True)
    password: Mapped[str]

    passwords: Mapped[List[Password]] = relationship(Password, back_populates="user")
