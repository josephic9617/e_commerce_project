from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_admin
from app.models.currency import Currency
from app.models.user import User
from app.schemas.currency import CurrencyUpdate, CurrencyResponse

router = APIRouter(prefix="/currency", tags=["Currency"])


@router.get("/", response_model=CurrencyResponse)
def get_currency(db: Session = Depends(get_db)):
    currency = db.query(Currency).first()
    if not currency:
        # Create default
        currency = Currency(usd_to_tmt=3.5)
        db.add(currency)
        db.commit()
        db.refresh(currency)
    return currency


@router.put("/", response_model=CurrencyResponse)
def update_currency(
    data: CurrencyUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    currency = db.query(Currency).first()
    if not currency:
        currency = Currency(usd_to_tmt=data.usd_to_tmt)
        db.add(currency)
    else:
        currency.usd_to_tmt = data.usd_to_tmt

    db.commit()
    db.refresh(currency)
    return currency
