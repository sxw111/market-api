from app.models import MarketBase


class TokenData(MarketBase):
    id: int | None = None


class TokenResponse(MarketBase):
    access_token: str
    token_type: str
