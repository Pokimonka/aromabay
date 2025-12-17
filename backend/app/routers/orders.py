from fastapi import APIRouter, Depends, BackgroundTasks, Request
from faststream import response
from sqlalchemy.orm import Session
from typing import List
import pika

from app.broker import publish_order
from .users import get_current_user
from ..database import get_db
from .. import crud, schemas, models
from ..schemas import OrderItemResponse

router = APIRouter(prefix="/orders", tags=["orders"])

connection_params = pika.ConnectionParameters(
    host="localhost",
    port=5672
)

def send_order_notification(order_data: dict):
    """Отправка уведомления в RabbitMQ через брокер"""
    # Используем функцию из брокера вместо прямого pika
    print("send_order_noti")
    publish_order(order_data)

@router.post("/", response_model=schemas.OrderResponse)
def create_order(
        order: schemas.OrderCreate,
        background_tasks: BackgroundTasks,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    # Создаем заказ
    user_id = current_user.id
    db_order = crud.create_order(db=db, order=order, user_id=user_id)
    print(db_order)
    # Отправляем уведомление в фоне
    order_data = {
        "id": db_order.id,
        "status": db_order.status,
        "total_amount": db_order.total_amount,
        "telegram_username": current_user.telegram_username,
        "user_email": current_user.email,
        "items": [{"id": db_order.id, "perfume_id": item.perfume_id, "quantity": item.quantity, "price": item.price} for item in order.items]
    }
    print(order_data)
    print("отправляем уведомление в фоне")
    background_tasks.add_task(send_order_notification, order_data)

    return order_data


@router.get("/", response_model=List[schemas.OrderResponse])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders
