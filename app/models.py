from pydantic import BaseModel


# Pydantic models base class
class MarketBase(BaseModel):
    class Config:
        from_attributes = True
