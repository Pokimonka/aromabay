from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class PerfumeType(enum.Enum):
    FLORAL = "floral"
    WOODY = "woody"
    ORIENTAL = "oriental"
    FRESH = "fresh"
    CITRUS = "citrus"
    GOURMAND = "gourmand"
    AQUATIC = "aquatic"
    CHYPRE = "chypre"
    FOUGERE = "fougere"

class Perfume(Base):
    __tablename__ = "perfumes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    brand = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    perfume_type = Column(Enum(PerfumeType), nullable=False)
    description =Column(Text)
    img_url = Column(String(200))
    stock_quantity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(100), nullable=False)
    user_name = Column(String(100))
    user_phone = Column(String(20))
    total_amount = Column(Float, nullable=False)
    status = Column(String(20), default="pending")  # pending, confirmed, shipped, delivered, cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связь с элементами заказа
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    perfume_id = Column(Integer, ForeignKey("perfumes.id"))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)  # Цена на момент заказа

    # Связи
    order = relationship("Order", back_populates="items")
    perfume = relationship("Perfume")