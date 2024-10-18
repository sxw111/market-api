from pydantic import EmailStr
from sqlalchemy.orm import Mapped, mapped_column

from app.database.core import Base
from app.models import MarketBase


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(unique=False, nullable=True)
    google_id: Mapped[str] = mapped_column(unique=True, index=True, nullable=True)


class UserBase(MarketBase):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserCreateGoogle(UserBase):
    google_id: str


class UserRead(UserBase):
    id: int
