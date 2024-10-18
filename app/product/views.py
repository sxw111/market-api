from typing import Any

from fastapi import APIRouter, HTTPException, Query, status

from app.category.service import get as get_category
from app.database.core import SessionDep

from .models import ProductCreate, ProductRead, ProductUpdate
from .service import (
    create,
    delete,
    get,
    get_all,
    get_by_name,
    get_products_by_category,
    update,
)

router = APIRouter()


@router.get("/", response_model=list[ProductRead])
async def get_products(
    db_session: SessionDep,
    min_price: float | None = Query(None, description="Min price"),
    max_price: float | None = Query(None, description="Max price"),
    category_ids: list[int] | None = Query(None, description="Categories list"),
) -> Any:
    products = await get_all(
        db_session=db_session,
        min_price=min_price,
        max_price=max_price,
        category_ids=category_ids,
    )

    if products == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Products were not found."
        )

    return products


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(db_session: SessionDep, product_id: int) -> Any:
    product = await get(db_session=db_session, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id `{product_id}` does not exist.",
        )

    return product


@router.get(
    "/category{category_id}",
    response_model=list[ProductRead],
    status_code=status.HTTP_200_OK,
)
async def get_by_category(db_session: SessionDep, category_id: int) -> Any:
    category = await get_category(db_session=db_session, category_id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id `{category_id}` does not exist.",
        )

    products = await get_products_by_category(
        db_session=db_session, category_id=category_id
    )

    if products == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Products related to category ID: {category_id} not found.",
        )

    return products


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    db_session: SessionDep,
    product_in: ProductCreate,
) -> Any:
    product = await get_by_name(db_session=db_session, product_name=product_in.name)
    if product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with name `{product_in.name}` already exists.",
        )

    category = await get_category(
        db_session=db_session, category_id=product_in.category_id
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id `{product_in.category_id}` does not exist.",
        )

    product = await create(db_session=db_session, product_in=product_in)

    return product


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    db_session: SessionDep,
    product_id: int,
    product_in: ProductUpdate,
) -> Any:
    product = await get(db_session=db_session, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id `{product_id}` does not exist.",
        )

    product_db = await get_by_name(
        db_session=db_session, product_name=product_in.name  # type: ignore
    )
    if product_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with name `{product_in.name}` already exists.",
        )

    category = await get_category(
        db_session=db_session, category_id=product_in.category_id  # type: ignore
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id `{product_in.category_id}` does not exist.",
        )

    product = await update(
        db_session=db_session, product=product, product_in=product_in
    )

    return product


@router.delete("/{product_id}", response_model=None)
async def delete_product(db_session: SessionDep, product_id: int) -> None:
    product = await get(db_session=db_session, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id `{product_id}` does not exist.",
        )
    await delete(db_session=db_session, product_id=product_id)
