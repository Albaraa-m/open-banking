from dataclasses import dataclass
from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base

if TYPE_CHECKING:
    from models.bank_connection import BankConnection


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    customer_id: Mapped[str | None] = mapped_column(String(64), unique=True)

    bank_connections: Mapped[List["BankConnection"]] = relationship(
        back_populates="user"
    )
