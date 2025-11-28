from pydantic import EmailStr
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
    volume = Column(Integer, default=50)
    concentration = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # INSERT INTO perfumes (name, brand, price, perfume_type, description, stock_quantity, volume, concentration, )
    # VALUES('DUH', 'BRAND', 5000, 'fresh', 'AHUENNIE OTVECHAU', 10, 50, 'idf');

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    total_amount = Column(Float, nullable=False)
    status = Column(String(20), default="pending")  # pending, confirmed, shipped, delivered, cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # Связь с элементами заказа
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    user = relationship("User", back_populates="orders")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    perfume_id = Column(Integer, ForeignKey("perfumes.id", ondelete="CASCADE"))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)  # Цена на момент заказа
    # Связи
    order = relationship("Order", back_populates="items")
    perfume = relationship("Perfume")

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # Связь с элементами заказа
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")
    user = relationship("User", back_populates="carts")

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"))
    perfume_id = Column(Integer, ForeignKey("perfumes.id", ondelete="CASCADE"))
    quantity = Column(Integer, nullable=False)
    # Связи
    cart = relationship("Cart", back_populates="items")
    perfume = relationship("Perfume")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    telegram_username = Column(String, nullable=True)
    role = Column(String(20), default="customer")  # customer, admin
    hashed_password = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), onupdate=func.now())

    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    carts = relationship("Cart", back_populates="user", cascade="all, delete-orphan")

class UserSession(Base):
    __tablename__ = "user_sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    session_token = Column(String(100), unique=True)
    created_at = Column(DateTime(timezone=True), onupdate=func.now())
    expires_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User")
