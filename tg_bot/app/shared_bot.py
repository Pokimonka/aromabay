from aiogram import Bot
import os

# Глобальный бот для отправки сообщений
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN", "8295415758:AAHiUC12K2lqngvaKrh8kpTICcdSjhe8weU"))

# Список ID админов (замени на реальные)
ADMIN_IDS = [6473177486]


async def send_to_admins(message: str, parse_mode: str = "Markdown"):
    """Отправка сообщения всем админам"""
    success_count = 0
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, message, parse_mode=parse_mode)
            success_count += 1
            print(f"✅ Message sent to admin {admin_id}")
        except Exception as e:
            print(f"❌ Failed to send message to admin {admin_id}: {e}")

    return success_count > 0


async def send_to_admin(admin_id: int, message: str, parse_mode: str = "Markdown"):
    """Отправка сообщения конкретному админу"""
    try:
        await bot.send_message(admin_id, message, parse_mode=parse_mode)
        print(f"✅ Message sent to admin {admin_id}")
        return True
    except Exception as e:
        print(f"❌ Failed to send message to admin {admin_id}: {e}")
        return False


async def send_to_user(user_id: int, message: str, parse_mode: str = "Markdown"):
    """Отправка сообщения конкретному пользователю"""
    try:
        await bot.send_message(user_id, message, parse_mode=parse_mode)
        return True
    except Exception as e:
        print(f"❌ Failed to send message to user {user_id}: {e}")
        return False