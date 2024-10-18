from fastapi import APIRouter

from app.auth.google_auth import google_auth_router
from app.auth.views import auth_router
from app.category.views import router as categories_router
from app.product.views import router as products_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(google_auth_router, prefix="/google", tags=["google auth"])
api_router.include_router(categories_router, prefix="/categories", tags=["categories"])
api_router.include_router(products_router, prefix="/products", tags=["products"])


@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
