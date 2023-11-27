from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.base import Base

if TYPE_CHECKING:
    from db.passwords.models import Password

class User(Base):

    user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4(), server_default=str(uuid.uuid4()))
    login: Mapped[str] = mapped_column(String(15), unique=True, index=True)
    password: Mapped[str]
    passwords: Mapped[List[Password]] = relationship(back_populates='user')