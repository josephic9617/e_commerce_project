from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import engine
from app.core.security import hash_password
from app.models.base import Base
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.models.currency import Currency
from app.routers import auth, categories, products, orders, currency, reports, upload, users

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Commerce API",
    description="E-Commerce REST API - FastAPI + SQLite",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded images
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
app.include_router(currency.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
app.include_router(upload.router, prefix="/api")
app.include_router(users.router, prefix="/api")


@app.on_event("startup")
def create_admin():
    """Create default admin user on startup if not exists."""
    from app.core.database import SessionLocal

    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.phone == settings.ADMIN_PHONE).first()
        if not admin:
            admin = User(
                phone=settings.ADMIN_PHONE,
                password_hash=hash_password(settings.ADMIN_PASSWORD),
                full_name="Admin",
                is_admin=True,
            )
            db.add(admin)
            db.commit()
            print(f"Admin ulanyjy döredildi: {settings.ADMIN_PHONE}")

        # Create default currency if not exists
        cur = db.query(Currency).first()
        if not cur:
            cur = Currency(usd_to_tmt=3.5)
            db.add(cur)
            db.commit()
            print("Default walýuta kursy döredildi: 1 USD = 3.5 TMT")
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "E-Commerce API işleýär!", "docs": "/docs"}
