from pydantic import BaseModel
from datetime import datetime


class CurrencyUpdate(BaseModel):
    usd_to_tmt: float


class CurrencyResponse(BaseModel):
    id: int
    usd_to_tmt: float
    updated_at: datetime

    class Config:
        from_attributes = True
