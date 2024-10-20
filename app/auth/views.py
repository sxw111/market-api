from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.database.core import SessionDep
from app.jwt.models import TokenResponse
from app.security import create_access_token, verify_password

from .models import UserCreate, UserRead
from .service import create, get_by_email
from .utils import verify_email_with_hunter

auth_router = APIRouter()


@auth_router.post(
    "/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED
)
async def signup(db_session: SessionDep, user_in: UserCreate) -> Any:
    """Creates a new user account."""
    user = await get_by_email(db_session=db_session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email `{user_in.email}` already exists.",
        )

    if not await verify_email_with_hunter(email=user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The email address provided is not valid.",
        )

    user = await create(db_session=db_session, user_in=user_in)

    return user


@auth_router.post(
    "/signin", response_model=TokenResponse, status_code=status.HTTP_200_OK
)
async def signin(
    db_session: SessionDep, user_credentials: OAuth2PasswordRequestForm = Depends()
) -> TokenResponse:
    """Authenticates a user and provides an access token."""
    user = await get_by_email(db_session=db_session, email=user_credentials.username)

    if user and verify_password(user_credentials.password, user.password):
        data = {"user_id": user.id}
        access_token = create_access_token(data=data)

        return TokenResponse(access_token=access_token, token_type="bearer")

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password.",
        headers={"WWW-Authenticate": "Bearer"},
    )
