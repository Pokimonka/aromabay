from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

# Perfume CRUD
def get_perfumes(db: Session, skip: int = 0, limit: int = 100) -> List[models.Perfume]:
    return db.query(models.Perfume).filter(models.Perfume.is_active == True).offset(skip).limit(limit).all()

def get_perfume(db: Session, perfume_id: int) -> Optional[models.Perfume]:
    return db.query(models.Perfume).filter(models.Perfume.id == perfume_id, models.Perfume.is_active == True).first()

def create_perfume(db: Session, perfume: schemas.PerfumeCreate) -> models.Perfume:
    db_perfume = models.Perfume(**perfume.dict())
    db.add(db_perfume)
    db.commit()
    db.refresh(db_perfume)
    return db_perfume

# Order CRUD
def create_order(db: Session, order: schemas.OrderCreate) -> models.Order:
    # Создаем заказ
    db_order = models.Order(
        user_email=order.user_email,
        user_name=order.user_name,
        user_phone=order.user_phone,
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