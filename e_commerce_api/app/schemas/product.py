from pydantic import BaseModel
from datetime import datetime


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price_usd: float
    category_id: int
    image_url: str | None = None
    stock: int = 0
    is_active: bool = True
    translations: dict | None = None


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price_usd: float | None = None
    category_id: int | None = None
    image_url: str | None = None
    stock: int | None = None
    is_active: bool | None = None
    translations: dict | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price_usd: float
    category_id: int
    category_name: str | None = None
    image_url: str | None = None
    stock: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    translations: dict | None = None

    class Config:
        from_attributes = True


class PaginatedProducts(BaseModel):
    items: list[ProductResponse]
    total: int
    page: int
    pages: int
    per_page: int
