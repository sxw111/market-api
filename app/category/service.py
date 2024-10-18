from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import Category, CategoryCreate, CategoryUpdate


async def get(*, db_session: AsyncSession, category_id: int) -> Category | None:
    result = await db_session.execute(
        select(Category).where(Category.id == category_id)
    )

    return result.scalars().first()


async def get_by_name(
    *, db_session: AsyncSession, category_name: str
) -> Category | None:
    result = await db_session.execute(
        select(Category).where(Category.name == category_name)
    )

    return result.scalars().first()


async def get_all(*, db_session: AsyncSession) -> list[Category]:
    result = await db_session.execute(select(Category))

    return result.scalars().all()  # type: ignore


async def create(*, db_session: AsyncSession, category_in: CategoryCreate) -> Category:
    category = Category(**category_in.model_dump())

    db_session.add(category)
    await db_session.commit()
    await db_session.refresh(category)

    return category


async def update(
    *, db_session: AsyncSession, category: Category, category_in: CategoryUpdate
) -> Category:
    category_data = category.dict()
    update_data = category_in.model_dump(exclude_unset=True)
    for field in category_data:
        if field in update_data:
            setattr(category, field, update_data[field])

    await db_session.commit()
    await db_session.refresh(category)

    return category


async def delete(*, db_session: AsyncSession, category_id: int) -> None:
    result = await db_session.execute(
        select(Category).where(Category.id == category_id)
    )
    category = result.scalars().first()
    await db_session.delete(category)
    await db_session.commit()
