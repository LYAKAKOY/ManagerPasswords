import uuid
from typing import List

from cryptography.fernet import Fernet
from db.base import Base
from db.passwords.models import Password
from sqlalchemy import LargeBinary
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class User(Base):

    user_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4(), server_default=uuid.uuid4().hex
    )
    login: Mapped[str] = mapped_column(String(15), unique=True, index=True)
    password: Mapped[str]
    master_password: Mapped[bytes] = mapped_column(
        LargeBinary,
        default=Fernet.generate_key(),
        server_default=Fernet.generate_key().decode("utf-8"),
    )

    passwords: Mapped[List[Password]] = relationship(Password, back_populates="user")
