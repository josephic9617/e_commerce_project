from pydantic import BaseModel, field_validator
import re


class UserRegister(BaseModel):
    phone: str
    password: str
    full_name: str | None = None
    otp_code: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        pattern = r"^\+9936\d{7}$"
        if not re.match(pattern, v):
            raise ValueError("Telefon belgisi +9936XXXXXXX formatynda bolmaly")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Parol iň az 6 simwol bolmaly")
        return v


class SendOTPRequest(BaseModel):
    phone: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        pattern = r"^\+9936\d{7}$"
        if not re.match(pattern, v):
            raise ValueError("Telefon belgisi +9936XXXXXXX formatynda bolmaly")
        return v


class UserLogin(BaseModel):
    phone: str
    password: str


class UserResponse(BaseModel):
    id: int
    phone: str
    full_name: str | None = None
    is_admin: bool
    is_active: bool

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class UserStatusUpdate(BaseModel):
    is_active: bool
