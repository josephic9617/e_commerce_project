from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from datetime import datetime, timezone, timedelta

from app.core.database import get_db
from app.core.deps import get_current_admin
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.models.category import Category

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/sales")
def get_sales_report(
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    query = db.query(Order).filter(Order.status != "cancelled")

    if start_date:
        query = query.filter(Order.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(Order.created_at <= datetime.fromisoformat(end_date))

    orders = query.all()

    total_orders = len(orders)
    total_usd = sum(o.total_usd for o in orders)
    total_tmt = sum(o.total_tmt for o in orders)

    status_counts = {}
    for order in orders:
        status_counts[order.status] = status_counts.get(order.status, 0) + 1

    return {
        "total_orders": total_orders,
        "total_usd": round(total_usd, 2),
        "total_tmt": round(total_tmt, 2),
        "status_breakdown": status_counts,
    }


@router.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    total_products = db.query(Product).count()
    total_categories = db.query(Category).count()
    total_users = db.query(User).filter(User.is_admin == False).count()
    total_orders = db.query(Order).count()
    pending_orders = db.query(Order).filter(Order.status == "pending").count()

    revenue_usd = (
        db.query(func.sum(Order.total_usd))
        .filter(Order.status != "cancelled")
        .scalar()
        or 0
    )
    revenue_tmt = (
        db.query(func.sum(Order.total_tmt))
        .filter(Order.status != "cancelled")
        .scalar()
        or 0
    )

    # Top selling products
    top_products = (
        db.query(
            OrderItem.product_name,
            func.sum(OrderItem.quantity).label("total_qty"),
            func.sum(OrderItem.price_usd * OrderItem.quantity).label("total_revenue"),
        )
        .group_by(OrderItem.product_name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(5)
        .all()
    )

    return {
        "total_products": total_products,
        "total_categories": total_categories,
        "total_users": total_users,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "revenue_usd": round(revenue_usd, 2),
        "revenue_tmt": round(revenue_tmt, 2),
        "top_products": [
            {
                "name": p.product_name,
                "total_qty": p.total_qty,
                "total_revenue": round(p.total_revenue, 2),
            }
            for p in top_products
        ],
        "daily_sales": [
            {"date": str(d[0]), "revenue": round(float(d[1]), 2)}
            for d in db.query(
                cast(Order.created_at, Date),
                func.sum(Order.total_usd)
            )
            .filter(Order.status != "cancelled")
            .filter(Order.created_at >= datetime.now(timezone.utc) - timedelta(days=7))
            .group_by(cast(Order.created_at, Date))
            .order_by(cast(Order.created_at, Date))
            .all()
        ],
        "status_breakdown": {
            s: c for s, c in db.query(Order.status, func.count(Order.id))
            .group_by(Order.status)
            .all()
        }
    }
