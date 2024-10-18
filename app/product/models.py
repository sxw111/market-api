from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.category.models import Category
from app.database.core import Base
from app.models import MarketBase


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, unique=False, nullable=True)
    price: Mapped[float] = mapped_column(unique=False, nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates="products")


class ProductBase(MarketBase):
    name: str
    price: float


class ProductCreate(ProductBase):
    description: str | None
    category_id: int


class ProductRead(ProductBase):
    id: int
    description: str | None
    category_id: int


class ProductUpdate(ProductBase):
    name: str | None  # type: ignore
    description: str | None
    price: float | None  # type: ignore
    category_id: int | None
