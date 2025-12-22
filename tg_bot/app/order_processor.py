import aio_pika
import json
import asyncpg
import os

class OrderProcessor:
    def __init__(self):
        self.rabbitmq_url = os.getenv("RABBITMQ_URL")
        self.database_url = os.getenv("DATABASE_URL")
        self.connection = None
        self.channel = None

    async def connect(self):
        """Подключение к RabbitMQ"""
        try:
            self.connection = await aio_pika.connect_robust(self.rabbitmq_url, reconnect_interval=5)
            self.channel = await self.connection.channel()
            print("OrderProcessor connected to RabbitMQ")
            return True
        except Exception as e:
            print(f"OrderProcessor connection failed: {e}")
            return False

    async def send_notification(self, notification_data: dict):
        """Отправка уведомления в очередь notifications"""
        try:
            await self.channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps(notification_data).encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key="notifications"
            )
        except Exception as e:
            print(f"Failed to send notification: {e}")

    async def process_order(self, order_data: dict):
        """Обработка одного заказа"""
        print(f"Processing order: {order_data}")

        conn = await asyncpg.connect(self.database_url)
        try:
            order_id = order_data.get("id")
            print(order_id)
            print(type(order_id))
            # Получаем заказ из БД
            order = await conn.fetchrow(
                "SELECT * FROM orders WHERE id = $1", order_id
            )
            if not order:
                print(f"❌ Order {order_id} not found")
                return

            # Получаем товары заказа
            order_items = await conn.fetch(
                "SELECT oi.*, p.name as perfume_name, p.stock_quantity "
                "FROM order_items oi "
                "JOIN perfumes p ON p.id = oi.perfume_id "
                "WHERE oi.order_id = $1", order_id
            )

            # Проверяем наличие товаров
            all_in_stock = True
            for item in order_items:
                if item['stock_quantity'] < item['quantity']:
                    all_in_stock = False
                    print(f"❌ Not enough stock for {item['perfume_name']}")
                    return

            # Обновляем статус заказа
            if all_in_stock:
                # Резервируем товары
                for item in order_items:
                    await conn.execute(
                        "UPDATE perfumes SET stock_quantity = stock_quantity - $1 WHERE id = $2",
                        item['quantity'], item['perfume_id']
                    )

                await conn.execute(
                    "UPDATE orders SET status = 'confirmed' WHERE id = $1",
                    order_id
                )
                print(f"✅ Order {order_id} confirmed")

                # Отправляем уведомление о подтверждении
                await self.send_notification({
                    "type": "order_processed",
                    "order_id": order_id,
                    "status": order['status'],
                    "user_email": order_data['user_email'],
                    "telegram_username": order_data['telegram_username'],
                    "total_amount": order['total_amount']
                })

            else:
                await conn.execute(
                    "UPDATE orders SET status = 'cancelled' WHERE id = $1",
                    order_id
                )
                print(f"Order {order_id} cancelled due to insufficient stock")

                # Отправляем уведомление об отмене
                await self.send_notification({
                    "type": "order_processed",
                    "order_id": order_id,
                    "status": "cancelled",
                    "user_email": order['user_email'],
                    "telegram_username": order['telegram_username'],
                    "total_amount": order['total_amount']
                })

        except Exception as e:
            print(f"Error processing order: {e}")
        finally:
            await conn.close()

    async def start_consuming(self):
        """Запуск обработки заказов"""
        try:
            if not await self.connect():
                return

            queue = await self.channel.declare_queue("orders", durable=True)

            print("OrderProcessor started. Waiting for orders...")

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        try:
                            order_data = json.loads(message.body.decode())
                            await self.process_order(order_data)
                        except Exception as e:
                            print(f"Error processing message: {e}")

        except Exception as e:
            print(f"❌ OrderProcessor error: {e}")

    async def close(self):
        """Закрытие подключения"""
        if self.connection:
            await self.connection.close()


# Глобальный экземпляр
order_processor = OrderProcessor()


async def start_order_processor():
    """Функция для запуска из main.py"""
    await order_processor.start_consuming()