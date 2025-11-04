import aio_pika
import json
import os

from .shared_bot import send_to_admins
from .message_templates import (
    order_processed_template,
    order_confirmed_by_admin_template,
    low_stock_template,
    new_order_created_template
)

class NotificationSender:
    def __init__(self):
        self.rabbitmq_url = os.getenv("RABBITMQ_URL")
        self.connection = None
        self.channel = None

    async def connect(self):
        """Подключение к RabbitMQ"""
        try:
            print(self.rabbitmq_url)
            self.connection = await aio_pika.connect_robust(self.rabbitmq_url, reconnect_interval=5)
            self.channel = await self.connection.channel()
            print("NotificationSender connected to RabbitMQ")
            return True
        except Exception as e:
            print(f"NotificationSender connection failed: {e}")
            return False

    async def process_notification(self, message_data: dict):
        """Обработка одного уведомления"""
        try:
            notification_type = message_data.get("type")
            print(f"🔔 Processing notification: {notification_type}")

            if notification_type == "order_processed":
                await self._handle_order_processed(message_data)
            elif notification_type == "order_created":
                await self._handle_order_created(message_data)
            elif notification_type == "order_confirmed_by_admin":
                await self._handle_admin_confirmation(message_data)
            elif notification_type == "low_stock":
                await self._handle_low_stock(message_data)
            else:
                print(f"Unknown notification type: {notification_type}")

        except Exception as e:
            print(f"Error processing notification: {e}")

    async def _handle_order_processed(self, data: dict):
        """Обработка уведомления о processed заказе"""
        order_id = data.get("order_id")
        status = data.get("status")
        user_email = data.get("user_email")
        user_name = data.get("user_name")
        total_amount = data.get("total_amount")

        telegram_message = order_processed_template(
            order_id, status, user_name, user_email, total_amount
        )

        await send_to_admins(telegram_message)
        print(f"Order processed notification sent for order #{order_id}")

    async def _handle_order_created(self, data: dict):
        """Обработка уведомления о новом созданном заказе"""
        order_id = data.get("order_id")
        user_email = data.get("user_email")
        user_name = data.get("user_name")
        total_amount = data.get("total_amount")

        telegram_message = new_order_created_template(
            order_id, user_name, user_email, total_amount
        )

        await send_to_admins(telegram_message)
        print(f"New order notification sent for order #{order_id}")

    async def _handle_admin_confirmation(self, data: dict):
        """Обработка подтверждения заказа админом"""
        order_id = data.get("order_id")
        admin_name = data.get("admin_name", "Администратор")

        telegram_message = order_confirmed_by_admin_template(order_id, admin_name)
        await send_to_admins(telegram_message)
        print(f"Admin confirmation notification sent for order #{order_id}")

    async def _handle_low_stock(self, data: dict):
        """Обработка уведомления о низком запасе"""
        perfume_name = data.get("perfume_name")
        stock_quantity = data.get("stock_quantity")

        telegram_message = low_stock_template(perfume_name, stock_quantity)
        await send_to_admins(telegram_message)
        print(f"Low stock notification sent for {perfume_name}")

    async def start_consuming(self):
        """Запуск потребления уведомлений"""
        try:
            if not await self.connect():
                return

            queue = await self.channel.declare_queue("notifications", durable=True)

            print("NotificationSender started. Waiting for notifications...")

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        try:
                            message_data = json.loads(message.body.decode())
                            await self.process_notification(message_data)
                        except Exception as e:
                            print(f"Error processing message: {e}")

        except Exception as e:
            print(f"NotificationSender error: {e}")

    async def close(self):
        """Закрытие подключения"""
        if self.connection:
            await self.connection.close()
            print("NotificationSender disconnected")

# Создаем глобальный экземпляр
notification_sender = NotificationSender()

async def start_notification_sender():
    """Функция для запуска из main.py"""
    await notification_sender.start_consuming()