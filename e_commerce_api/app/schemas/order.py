from pydantic import BaseModel, field_validator
from datetime import datetime
import re


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v: int) -> int:
        if v < 1:
            raise ValueError("Mukdar iň az 1 bolmaly")
        return v


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    price_usd: float
    price_tmt: float

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    items: list[OrderItemCreate]
    guest_phone: str | None = None
    guest_name: str | None = None
    address: str | None = None
    note: str | None = None

    @field_validator("guest_phone")
    @classmethod
    def validate_phone(cls, v: str | None) -> str | None:
        if v is not None:
            pattern = r"^\+99361\d{6}$"
            if not re.match(pattern, v):
                raise ValueError("Telefon belgisi +99361XXXXXX formatynda bolmaly")
        return v


class OrderStatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        allowed = ["pending", "confirmed", "shipped", "delivered", "cancelled"]
        if v not in allowed:
            raise ValueError(f"Status {allowed} bolmaly")
        return v


class OrderResponse(BaseModel):
    id: int
    user_id: int | None = None
    guest_phone: str | None = None
    guest_name: str | None = None
    status: str
    total_usd: float
    total_tmt: float
    address: str | None = None
    note: str | None = None
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemResponse] = []

    class Config:
        from_attributes = True


class PaginatedOrders(BaseModel):
    items: list[OrderResponse]
    total: int
    page: int
    pages: int
    per_page: int
