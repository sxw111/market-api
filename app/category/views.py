from typing import Any

from fastapi import APIRouter, HTTPException, status
from fastapi_cache.decorator import cache

from app.database.core import SessionDep

from .models import CategoryCreate, CategoryRead, CategoryUpdate
from .service import create, delete, get, get_all, get_by_name, update

router = APIRouter()


@router.get("/", response_model=list[CategoryRead])
@cache(expire=3600)
async def get_categories(db_session: SessionDep) -> Any:
    """Return all categories in the database."""
    return await get_all(db_session=db_session)


@router.get("/{category_id}", response_model=CategoryRead)
@cache(expire=3600)
async def get_category(db_session: SessionDep, category_id: int) -> Any:
    """Retrieve information about a category by its ID."""
    category = await get(db_session=db_session, category_id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id `{category_id}` does not exist.",
        )

    return category


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    db_session: SessionDep,
    category_in: CategoryCreate,
) -> Any:
    """Create a new category."""
    category = await get_by_name(db_session=db_session, category_name=category_in.name)
    if category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with name `{category_in.name}` already exists.",
        )

    category = await create(db_session=db_session, category_in=category_in)

    return category


@router.put("/{category_id}", response_model=CategoryRead)
async def update_category(
    db_session: SessionDep,
    category_id: int,
    category_in: CategoryUpdate,
) -> Any:
    """Update a category."""
    category = await get(db_session=db_session, category_id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id `{category_id}` does not exist.",
        )
    category = await update(
        db_session=db_session, category=category, category_in=category_in
    )

    return category


@router.delete("/{category_id}", response_model=None)
async def delete_category(db_session: SessionDep, category_id: int) -> None:
    """Delete a category."""
    category = await get(db_session=db_session, category_id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id `{category_id}` does not exist.",
        )
    await delete(db_session=db_session, category_id=category_id)
