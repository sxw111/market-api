from typing import TYPE_CHECKING

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.core import Base
from app.models import MarketBase

if TYPE_CHECKING:
    from app.product.models import Product


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, unique=False, nullable=True)
    products: Mapped[list["Product"]] = relationship(back_populates="category")


class CategoryBase(MarketBase):
    name: str


class CategoryCreate(CategoryBase):
    description: str | None


class CategoryRead(CategoryBase):
    id: int
    description: str | None


class CategoryUpdate(CategoryBase):
    name: str | None  # type: ignore
    description: str | None
