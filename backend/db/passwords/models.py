from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from db.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator

if TYPE_CHECKING:
    from db.users.models import User


class HexByteString(TypeDecorator, ABC):
    """Convert Python bytestring to string with hexadecimal digits and back for storage."""

    impl = String

    def process_bind_param(self, value, dialect):
        if not isinstance(value, bytes):
            raise TypeError("HexByteString columns support only bytes values.")
        return value.hex()

    def process_result_value(self, value, dialect):
        return bytes.fromhex(value) if value else None


class Password(Base):

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    service_name: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(HexByteString)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE")
    )

    user: Mapped[User] = relationship(back_populates="passwords")