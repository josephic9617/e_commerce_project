from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import math

from app.core.database import get_db
from app.core.deps import get_current_admin
from app.models.product import Product
from app.models.category import Category
from app.models.user import User
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    PaginatedProducts,
)

router = APIRouter(prefix="/products", tags=["Products"])


def _product_to_response(product: Product) -> ProductResponse:
    return ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        price_usd=product.price_usd,
        category_id=product.category_id,
        category_name=product.category.name if product.category else None,
        image_url=product.image_url,
        stock=product.stock,
        is_active=product.is_active,
        created_at=product.created_at,
        updated_at=product.updated_at,
    )


@router.get("/", response_model=PaginatedProducts)
def get_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(12, ge=1, le=100),
    category_id: int | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Product).filter(Product.is_active == True)

    if category_id:
        query = query.filter(Product.category_id == category_id)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    total = query.count()
    pages = math.ceil(total / per_page) if total > 0 else 1
    products = query.offset((page - 1) * per_page).limit(per_page).all()

    return PaginatedProducts(
        items=[_product_to_response(p) for p in products],
        total=total,
        page=page,
        pages=pages,
        per_page=per_page,
    )


@router.get("/all", response_model=PaginatedProducts)
def get_all_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(12, ge=1, le=100),
    category_id: int | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """Admin: get all products including inactive."""
    query = db.query(Product)

    if category_id:
        query = query.filter(Product.category_id == category_id)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    total = query.count()
    pages = math.ceil(total / per_page) if total > 0 else 1
    products = query.offset((page - 1) * per_page).limit(per_page).all()

    return PaginatedProducts(
        items=[_product_to_response(p) for p in products],
        total=total,
        page=page,
        pages=pages,
        per_page=per_page,
    )


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Haryt tapylmady")
    return _product_to_response(product)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    category = db.query(Category).filter(Category.id == data.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Kategoriýa tapylmady")

    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return _product_to_response(product)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Haryt tapylmady")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return _product_to_response(product)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Haryt tapylmady")

    db.delete(product)
    db.commit()
