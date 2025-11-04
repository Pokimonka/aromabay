import json
import os
from typing import Callable, Awaitable

import aio_pika
import pika
from aio_pika import Message, connect_robust
from dotenv import load_dotenv
from faststream import FastStream
from faststream.rabbit import RabbitBroker
load_dotenv(os.path.join('..', '.env'))
# URL для подключения к RabbitMQ
# rabbit_url = os.getenv(
#     "RABBITMQ_URL",
#     "amqp://guest:guest@rabbitmq:5672/"
# )
# FastStream брокер для асинхронных операций
broker = RabbitBroker()
app = FastStream(broker)

_is_connected = False

class AsyncRabbitMQClient:
    def __init__(self):
        self.url = os.getenv("RABBITMQ_URL")
        self.connection = None
        self.channel = None

    async def connect(self):
        """Асинхронное подключение к RabbitMQ"""
        try:
            self.connection = await connect_robust(self.url, reconnect_interval=5)
            self.channel = await self.connection.channel()
            print("✅ RabbitMQ connected (async)")
            return True
        except Exception as e:
            print(f"❌ RabbitMQ connection failed: {e}")
            return False

    async def close(self):
        """Асинхронное закрытие подключения"""
        if self.connection:
            await self.connection.close()
            print("✅ RabbitMQ disconnected (async)")

    async def publish(self, queue: str, message: dict):
        """Асинхронная публикация сообщения"""
        try:
            print("async publish")
            if not self.channel:
                await self.connect()
            print(f"async publish queue: {queue}")

            # Объявляем очередь
            await self.channel.declare_queue(queue, durable=True)
            print(f"async publish message: {message}")
            # Создаем и отправляем сообщение
            message_body = json.dumps(message).encode()
            print(f"async publish message_body: {message_body}")

            rabbit_message = Message(
                message_body,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            )
            print(f"async publish rabbit_message: {rabbit_message}")

            await self.channel.default_exchange.publish(
                rabbit_message,
                routing_key=queue
            )

            print(f"✅ Message sent to {queue}: {message}")
            return True

        except Exception as e:
            print(f"❌ Failed to publish message to {queue}: {e}")
            return False

    async def consume(self, queue: str, callback: Callable[[dict], Awaitable[None]]):
        """Асинхронное потребление сообщений из очереди"""
        try:
            if not self.channel:
                await self.connect()

            declared_queue = await self.channel.declare_queue(queue, durable=True)

            print(f"✅ Started consuming from {queue}")

            async with declared_queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        try:
                            message_data = json.loads(message.body.decode())
                            await callback(message_data)
                        except Exception as e:
                            print(f"❌ Error in consumer callback: {e}")

        except Exception as e:
            print(f"❌ Failed to start consumer for {queue}: {e}")
            raise


# Глобальный асинхронный клиент
async_client = AsyncRabbitMQClient()

# Асинхронные функции для lifespan
async def connect_broker():
    return await async_client.connect()

async def close_broker():
    return await async_client.close()

async def publish_order_async(order_data: dict):
    """Асинхронная публикация заказа"""
    return await async_client.publish("orders", order_data)

async def publish_notification_async(notification_data: dict):
    """Асинхронная публикация уведомления"""
    return await async_client.publish("notifications", notification_data)

async def consume_orders(callback: Callable[[dict], Awaitable[None]]):
    """Потребление сообщений из очереди заказов"""
    return await async_client.consume("orders", callback)

async def consume_notifications(callback: Callable[[dict], Awaitable[None]]):
    """Потребление сообщений из очереди уведомлений"""
    return await async_client.consume("notifications", callback)

async def check_health():
    """Проверка здоровья брокера"""
    try:
        return await async_client.publish("health_check", {"test": "message"})
    except Exception:
        return False

# Синхронный клиент для BackgroundTasks
class SyncRabbitMQClient:
    def __init__(self):
        self.url = os.getenv("RABBITMQ_URL")
        self.connection_params = pika.URLParameters(self.url)

    def publish(self, queue: str, message: dict):
        """Синхронная публикация сообщения"""
        try:
            print("sync publish")
            connection = pika.BlockingConnection(self.connection_params)
            channel = connection.channel()
            print(f"sync publish channel {channel}")

            channel.queue_declare(queue=queue, durable=True)
            print(f"sync publish queue {queue}")

            channel.basic_publish(
                exchange="",
                routing_key=queue,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                )
            )
            print(f"sync publish message {message}")

            print(f"✅ Message sent to {queue}: {message}")
            connection.close()
            return True

        except Exception as e:
            print(f"❌ Failed to send message to {queue}: {e}")
            return False

sync_client = None

def get_sync_client():
    global sync_client
    if sync_client is None:
        sync_client = SyncRabbitMQClient()
    return sync_client

def publish_order(order_data: dict):
    """Синхронная публикация заказа (для BackgroundTasks)"""
    return get_sync_client.publish("orders", order_data)

def publish_notification(notification_data: dict):
    """Синхронная публикация уведомления (для BackgroundTasks)"""
    return get_sync_client.publish("notifications", notification_data)


async def declare_exchange(self, exchange_name: str, exchange_type: str = "direct"):
    """Объявление exchange"""
    try:
        if not self.channel:
            await self.connect()

        await self.channel.declare_exchange(
            exchange_name,
            type=exchange_type,
            durable=True
        )
        print(f"✅ Exchange declared: {exchange_name}")
        return True
    except Exception as e:
        print(f"❌ Failed to declare exchange: {e}")
        return False


async def bind_queue_to_exchange(self, queue: str, exchange: str, routing_key: str = ""):
    """Привязка очереди к exchange"""
    try:
        if not self.channel:
            await self.connect()

        declared_queue = await self.channel.declare_queue(queue, durable=True)
        await declared_queue.bind(exchange, routing_key)
        print(f"✅ Queue {queue} bound to {exchange} with key {routing_key}")
        return True
    except Exception as e:
        print(f"❌ Failed to bind queue: {e}")
        return False


# Функции для работы с exchanges
async def publish_to_exchange(self, exchange: str, message: dict, routing_key: str = ""):
    """Публикация сообщения в exchange"""
    try:
        if not self.channel:
            await self.connect()

        message_body = json.dumps(message).encode()
        rabbit_message = Message(
            message_body,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )

        await self.channel.default_exchange.publish(
            rabbit_message,
            exchange=exchange,
            routing_key=routing_key
        )

        print(f"✅ Message sent to exchange {exchange}: {message}")
        return True

    except Exception as e:
        print(f"❌ Failed to publish to exchange: {e}")
        return False
