from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import pika

from app.broker import publish_order
from ..database import get_db
from .. import crud, schemas

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
        db: Session = Depends(get_db)
):
    # Создаем заказ
    db_order = crud.create_order(db=db, order=order)
    print(db_order)
    # Отправляем уведомление в фоне
    order_data = {
        "order_id": db_order.id,
        "user_email": db_order.user_email,
        "total_amount": db_order.total_amount,
        "status": db_order.status
    }
    print("отправляем уведомление в фоне")
    background_tasks.add_task(send_order_notification, order_data)

    return db_order


@router.get("/", response_model=List[schemas.OrderResponse])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders
