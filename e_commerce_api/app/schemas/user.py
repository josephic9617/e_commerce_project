from pydantic import BaseModel, field_validator
import re


class UserRegister(BaseModel):
    phone: str
    password: str
    full_name: str | None = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        pattern = r"^\+99361\d{6}$"
        if not re.match(pattern, v):
            raise ValueError("Telefon belgisi +99361XXXXXX formatynda bolmaly")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Parol iň az 6 simwol bolmaly")
        return v


class UserLogin(BaseModel):
    phone: str
    password: str


class UserResponse(BaseModel):
    id: int
    phone: str
    full_name: str | None = None
    is_admin: bool

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
