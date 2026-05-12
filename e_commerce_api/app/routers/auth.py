from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, UserResponse, TokenResponse, SendOTPRequest
from app.core import redis_cache
import random

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/send-otp", status_code=status.HTTP_200_OK)
def send_otp(data: SendOTPRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.phone == data.phone).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu telefon belgisi eýýäm hasaba alnan",
        )
    
    otp = str(random.randint(1000, 9999))
    print(f"[SMS MOCK] {data.phone} belgisine iberilen kod: {otp}")
    
    # Store OTP in Redis for 5 minutes
    redis_cache.set_cache(f"otp:{data.phone}", otp, expire=300)
    return {"message": "SMS kody iberildi"}


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.phone == data.phone).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu telefon belgisi eýýäm hasaba alnan",
        )

    # Verify OTP
    cached_otp = redis_cache.get_cache(f"otp:{data.phone}")
    if not cached_otp or cached_otp != data.otp_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SMS kody nädogry ýa-da möhleti gutaran",
        )
    
    # Clear OTP after successful use
    redis_cache.delete_cache(f"otp:{data.phone}")

    user = User(
        phone=data.phone,
        password_hash=hash_password(data.password),
        full_name=data.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == data.phone).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Telefon ýa-da parol nädogry",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Siziň hasabyňyz blokirlenen",
        )

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
