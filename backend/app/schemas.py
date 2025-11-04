from pydantic import BaseModel, EmailStr
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

class PerfumeCreate(PerfumeBase):
    pass

class PerfumeResponse(PerfumeBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Cart Schemas
class CartItem(BaseModel):
    perfume_id: int
    quantity: int


class Cart(BaseModel):
    items: List[CartItem] = []


# Order Schemas
class OrderItemCreate(BaseModel):
    perfume_id: int
    quantity: int
    price: float


class OrderCreate(BaseModel):
    user_email: EmailStr
    user_name: str
    user_phone: str
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
    user_email: str
    user_name: str
    user_phone: str
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
