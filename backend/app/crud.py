import sqlalchemy
from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional, Any, Union

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

def get_stock_quantity(perfume_id: int, db: Session) -> int:
    perfume = db.query(models.Perfume).filter(models.Perfume.id == perfume_id).first()
    print(perfume.stock_quantity)
    return perfume.stock_quantity


def add_to_cart(db: Session, user_id: int, item_data: schemas.CartItemCreate) -> Union[models.Cart, str]:
    # кладем в корзину
    perfume_id = item_data.perfume_id
    stock_quantity = get_stock_quantity(perfume_id, db)
    cart = get_cart(db, user_id)

    if item_data.quantity > stock_quantity:
        return "OUT_OF_STOCK"

    existing_item =  get_cart_item(db, cart.id, perfume_id)

    if existing_item:
        if existing_item.quantity < stock_quantity:
            existing_item.quantity += item_data.quantity
        elif existing_item.quantity >= stock_quantity:
            return "OUT_OF_STOCK"
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
        new_quantity: int) -> Union[dict, str]:

    stock_quantity = get_stock_quantity(perfume_id, db)
    print(f"new_quantity, stock_quantity {new_quantity}, {stock_quantity}")
    if new_quantity > stock_quantity:
        return "OUT_OF_STOCK"

    cart = get_cart(db, user_id)

    existing_item = get_cart_item(db, cart.id, perfume_id)
    print(f"exist_it.qua: {existing_item.quantity}")
    if existing_item:
        if  0 < new_quantity <= stock_quantity:
            existing_item.quantity = new_quantity
            db.commit()
        else:
            return "OUT_OF_STOCK"

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

def get_user_by_email_or_us(db: Session, username='', email='') -> (Optional[models.User], Optional[models.User]):
    user_by_username = None
    user_by_email = None
    if username:
        user_by_username = db.query(models.User).filter(models.User.username==username).first()
    if email:
        user_by_email = db.query(models.User).filter(models.User.email==email).first()
    return user_by_username, user_by_email

def verify_user_password(db: Session, username: str, password: str):
    user = get_user_by_email_or_us(db, username)
    if not user:
        return False
    return verify_password(password, user.hashed_password)
