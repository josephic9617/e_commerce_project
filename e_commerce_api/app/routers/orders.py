from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import math

from app.core.database import get_db
from app.core.deps import get_current_user, get_current_admin, get_optional_user
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.currency import Currency
from app.models.user import User
from app.schemas.order import (
    OrderCreate,
    OrderStatusUpdate,
    OrderResponse,
    OrderItemResponse,
    PaginatedOrders,
)

router = APIRouter(prefix="/orders", tags=["Orders"])


def _order_to_response(order: Order) -> OrderResponse:
    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        guest_phone=order.guest_phone,
        guest_name=order.guest_name,
        status=order.status,
        total_usd=order.total_usd,
        total_tmt=order.total_tmt,
        address=order.address,
        note=order.note,
        created_at=order.created_at,
        updated_at=order.updated_at,
        items=[
            OrderItemResponse.model_validate(item) for item in order.items
        ],
    )


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    if not current_user and not data.guest_phone:
        raise HTTPException(
            status_code=400,
            detail="Myhman üçin telefon belgisi gerek",
        )

    if not data.items:
        raise HTTPException(status_code=400, detail="Sargytda haryt bolmaly")

    # Get current exchange rate
    currency = db.query(Currency).first()
    rate = currency.usd_to_tmt if currency else 3.5

    total_usd = 0.0
    order_items = []

    for item_data in data.items:
        product = db.query(Product).filter(Product.id == item_data.product_id).first()
        if not product:
            raise HTTPException(
                status_code=400,
                detail=f"Haryt ID={item_data.product_id} tapylmady",
            )
        if not product.is_active:
            raise HTTPException(
                status_code=400,
                detail=f"'{product.name}' häzir elýeterli däl",
            )
        if product.stock < item_data.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"'{product.name}' üçin ýeterlik ammarda ýok (bar: {product.stock})",
            )

        item_price_usd = product.price_usd
        item_price_tmt = round(product.price_usd * rate, 2)
        line_total = item_price_usd * item_data.quantity
        total_usd += line_total

        order_items.append(
            OrderItem(
                product_id=product.id,
                product_name=product.name,
                quantity=item_data.quantity,
                price_usd=item_price_usd,
                price_tmt=item_price_tmt,
            )
        )

        # Decrease stock
        product.stock -= item_data.quantity

    total_tmt = round(total_usd * rate, 2)

    order = Order(
        user_id=current_user.id if current_user else None,
        guest_phone=data.guest_phone if not current_user else None,
        guest_name=data.guest_name if not current_user else None,
        total_usd=round(total_usd, 2),
        total_tmt=total_tmt,
        address=data.address,
        note=data.note,
        items=order_items,
    )

    db.add(order)
    db.commit()
    db.refresh(order)
    return _order_to_response(order)


@router.get("/my", response_model=list[OrderResponse])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    orders = (
        db.query(Order)
        .filter(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )
    return [_order_to_response(o) for o in orders]


@router.get("/", response_model=PaginatedOrders)
def get_all_orders(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status_filter: str | None = Query(None, alias="status"),
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    query = db.query(Order)
    if status_filter:
        query = query.filter(Order.status == status_filter)

    total = query.count()
    pages = math.ceil(total / per_page) if total > 0 else 1
    orders = (
        query.order_by(Order.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return PaginatedOrders(
        items=[_order_to_response(o) for o in orders],
        total=total,
        page=page,
        pages=pages,
        per_page=per_page,
    )


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Sargyt tapylmady")
    return _order_to_response(order)


@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Sargyt tapylmady")

    order.status = data.status
    db.commit()
    db.refresh(order)
    return _order_to_response(order)
