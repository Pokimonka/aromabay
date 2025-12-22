from pydantic import BaseModel, EmailStr, Field, validator, field_validator
from typing import List, Optional
from datetime import datetime

from app.models import PerfumeType


class PerfumeBase(BaseModel):
    name: str
    brand: str
    price: float
    perfume_type: PerfumeType
    description: Optional[str] = None
    img_url: Optional[str] = None
    stock_quantity: int = 0
    volume: int = 0
    concentration: str

class PerfumeCreate(PerfumeBase):
    pass

class PerfumeResponse(PerfumeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CartItemCreate(BaseModel):
    perfume_id: int
    quantity: int = 1

class CartItemResponse(BaseModel):
    id: int
    perfume_id: int
    quantity: int
    perfume: PerfumeResponse

    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    id: int
    user_id: int
    items: List[CartItemResponse]

    class Config:
        from_attributes = True

class CartItemUpdate(BaseModel):
    quantity: int = Field(gt=0, description="Quantity must be greater than 0")

# Order Schemas
class OrderItemCreate(BaseModel):
    perfume_id: int
    quantity: int
    price: int

class OrderCreate(BaseModel):
    status:  Optional[str] = "Created"
    items: List[OrderItemCreate]


class OrderItemResponse(BaseModel):
    id: int
    perfume_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    status: str
    total_amount: float
    telegram_username: str
    user_email: str
    items: List[OrderItemResponse]

# Для создания пользователя (без id, без пароля)
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    telegram_username: Optional[str] = None
    phone: Optional[str] = None
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr] = None
    telegram_username: Optional[str] = None
    session_token: str
    message: str = "Success"

    class Config:
        from_attributes = True

# Для ответа API (без пароля, с id)
class UserResponse(BaseModel):
    id:int
    username: str
    email: EmailStr
    telegram_username: Optional[str] = None
    role: str

    class Config:
        from_attributes = True

class UserSessionBase(BaseModel):
    user_id: int
    session_token: str
    expires_at: datetime

class UserSessionCreate(UserSessionBase):
    pass

class UserSessionResponse(UserSessionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


