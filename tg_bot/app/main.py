import asyncio
import logging
import sys

from app.bot import start_bot
from app.notification_sender import start_notification_sender
from app.order_processor import start_order_processor  # ← ДОБАВИТЬ

async def main():
    """Запуск всех компонентов бота"""
    print("🚀 Starting AromaBay Bot Service...")
    await asyncio.gather(
            start_bot(),
            start_notification_sender(),
            start_order_processor()
        )
    # Запускаем все компоненты параллельно
    # try:
    #     # Запускаем все компоненты параллельно
    #     await asyncio.gather(
    #         start_bot(),
    #         start_notification_sender(),
    #         start_order_processor()
    #     )
    # except Exception as e:
    #     print(f"❌ Bot service failed: {e}")
    #     # Перезапуск через 10 секунд
    #     print("🔄 Restarting in 10 seconds...")
    #     await asyncio.sleep(10)
    #     await main()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())