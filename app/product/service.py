from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import Product, ProductCreate, ProductUpdate


async def get(*, db_session: AsyncSession, product_id: int) -> Product | None:
    """Returns a product based on the given id."""
    result = await db_session.execute(select(Product).where(Product.id == product_id))

    return result.scalars().first()


async def get_by_name(*, db_session: AsyncSession, product_name: str) -> Product | None:
    """Returns a product by its name."""
    result = await db_session.execute(
        select(Product).where(Product.name == product_name)
    )

    return result.scalars().first()


async def get_products_by_category(
    *, db_session: AsyncSession, category_id: int
) -> list[Product]:
    """Return all products from the database for a given category."""
    query = select(Product).where(Product.category_id == category_id)
    result = await db_session.execute(query)

    return result.scalars().all()  # type: ignore


async def get_all(
    *,
    db_session: AsyncSession,
    min_price: float | None,
    max_price: float | None,
    category_ids: list[int] | None
) -> list[Product] | None:
    """Return products from the database based on optional filters."""
    query = select(Product)

    if min_price is not None:
        query = query.where(Product.price >= min_price)
    if max_price is not None:
        query = query.where(Product.price <= max_price)

    if category_ids:
        query = query.where(Product.category_id.in_(category_ids))

    result = await db_session.execute(query)

    return result.scalars().all()  # type: ignore


async def create(*, db_session: AsyncSession, product_in: ProductCreate) -> Product:
    """Creates a new product."""
    product = Product(**product_in.model_dump())

    db_session.add(product)
    await db_session.commit()
    await db_session.refresh(product)

    return product


async def update(
    *, db_session: AsyncSession, product: Product, product_in: ProductUpdate
) -> Product:
    """Updates a product."""
    product_data = product.dict()
    update_data = product_in.model_dump(exclude_unset=True)
    for field in product_data:
        if field in update_data:
            setattr(product, field, update_data[field])

    await db_session.commit()
    await db_session.refresh(product)

    return product


async def delete(*, db_session: AsyncSession, product_id: int) -> None:
    """Deletes an existing product."""
    result = await db_session.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    await db_session.delete(product)
    await db_session.commit()
