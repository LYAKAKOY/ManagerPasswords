from __future__ import annotations

import uuid
from abc import ABC
from typing import TYPE_CHECKING

from db.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy import LargeBinary
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from db.users.models import User


class Password(Base):

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    service_name: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes] = mapped_column(LargeBinary)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE")
    )

    user: Mapped[User] = relationship(back_populates="passwords")