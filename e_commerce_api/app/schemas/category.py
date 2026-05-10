from pydantic import BaseModel
from datetime import datetime


class CategoryCreate(BaseModel):
    name: str
    image_url: str | None = None


class CategoryUpdate(BaseModel):
    name: str | None = None
    image_url: str | None = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    image_url: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
