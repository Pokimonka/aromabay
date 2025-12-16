import sqlalchemy
from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional, Any

from .models import Perfume, CartItem
from .password_utils import hash_password, verify_password


# Perfume CRUD
def get_perfumes(db: Session, skip: int = 0, limit: int = 100) -> list[type[Perfume]]:
    return db.query(models.Perfume).offset(skip).limit(limit).all()

def get_perfume(db: Session, perfume_id: int) -> Optional[models.Perfume]:
    return db.query(models.Perfume).filter(models.Perfume.id == perfume_id).first()

def create_perfume(db: Session, perfume: schemas.PerfumeCreate) -> models.Perfume:
    db_perfume = models.Perfume(**perfume.model_dump())
    db.add(db_perfume)
    db.commit()
    db.refresh(db_perfume)
    return db_perfume

def delete_perfume(db: Session, perfume_id: int):
    perfume = get_perfume(db, perfume_id)
    if perfume:
        db.delete(perfume)
        db.commit()
        return perfume
    return None

# Order CRUD
def create_order(db: Session, order: schemas.OrderCreate, user_id: int) -> models.Order:
    # Создаем заказ
    db_order = models.Order(
        user_id=user_id,
        status=order.status,
        total_amount=sum(item.price * item.quantity for item in order.items)
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Создаем элементы заказа
    for item in order.items:
        db_item = models.OrderItem(
            order_id=db_order.id,
            perfume_id=item.perfume_id,
            quantity=item.quantity,
            price=item.price
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session, skip: int = 0, limit: int = 100) -> List[models.Order]:
    return db.query(models.Order).order_by(models.Order.created_at.desc()).offset(skip).limit(limit).all()

#cart CRUD
def get_cart(db: Session, user_id: int):
    cart = db.query(models.Cart).filter(models.Cart.user_id == user_id).first()
    if not cart:
        cart = models.Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

def get_cart_items(db: Session, user_id: int):
    cart = get_cart(db, user_id)

    if not cart:
        return {"id":cart.id, "user_id": user_id, "items": []}

    cart_items = (db.query(models.CartItem)
                  .filter(models.CartItem.cart_id == cart.id)
                  .options(sqlalchemy.orm.joinedload(models.CartItem.perfume))
                  .all())

    return {"id":cart.id, "user_id": user_id, "items": cart_items}


def add_to_cart(db: Session, user_id: int, item_data: schemas.CartItemCreate) -> models.Cart:
    # Создаем заказ
    cart = get_cart(db, user_id)

    existing_item =  get_cart_item(db, cart.id, item_data.perfume_id)

    if existing_item:
        existing_item.quantity += item_data.quantity
    else:
        new_item = models.CartItem(
            cart_id = cart.id,
            perfume_id = item_data.perfume_id,
            quantity = item_data.quantity
        )
        db.add(new_item)
    db.commit()
    return cart


def update_perfume_quantity(
        db: Session,
        user_id: int,
        perfume_id: int,
        quantity: int):
    cart = get_cart(db, user_id)

    cart_item = get_cart_item(db, cart.id, perfume_id)

    if cart_item:
        cart_item.quantity = quantity
        db.commit()

    return get_cart_items(db, user_id)

def remove_item_from_cart(db: Session, user_id: int, perfume_id: int):
    cart = get_cart(db, user_id)

    cart_item = get_cart_item(db, cart.id, perfume_id)

    if cart_item:
        db.delete(cart_item)
        db.commit()

    return get_cart_items(db, user_id)

def remove_from_cart(db: Session, user_id: int):
    cart = get_cart(db, user_id)

    # cart_item = get_cart_item(db, cart.id)

    if cart:
        db.delete(cart)
        db.commit()

    return get_cart_items(db, user_id)

def get_cart_item(db: Session, cart_id: int, perfume_id: int):
    return (db.query(models.CartItem).
                 filter(models.CartItem.cart_id == cart_id,
                        models.CartItem.perfume_id == perfume_id)
                 .first())

#user CRUD
def create_user(db: Session, new_user_data: schemas.UserRegister) -> models.User :
    hashed_password = hash_password(new_user_data.password).decode('utf-8')

    user = models.User(
        username = new_user_data.username,
        email = new_user_data.email,
        telegram_username = new_user_data.telegram_username,
        hashed_password = hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email_or_us(db: Session, username='', email='') -> Optional[models.User]:
    if username:
        user = db.query(models.User).filter(models.User.username==username).first()
    else:
        user = db.query(models.User).filter(models.User.email==email).first()
    return user

def verify_user_password(db: Session, username: str, password: str):
    user = get_user_by_email_or_us(db, username)
    if not user:
        return False
    return verify_password(password, user.hashed_password)
