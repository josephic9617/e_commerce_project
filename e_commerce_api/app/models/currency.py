from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime, timezone

from app.models.base import Base


class Currency(Base):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True, index=True)
    usd_to_tmt = Column(Float, nullable=False, default=3.5)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
