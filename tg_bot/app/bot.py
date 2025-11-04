import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncpg
from .shared_bot import send_to_admins

TOKEN = os.getenv(str("TELEGRAM_BOT_TOKEN"))
# Инициализация бота и диспетчера

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список ID админов (замени на реальные)
ADMIN_IDS = [6473177486, 6790135401]

def is_admin(user_id: int) -> bool:
    """Проверяет, является ли пользователь админом"""
    print(user_id)
    print(user_id in ADMIN_IDS)
    return user_id in ADMIN_IDS


async def get_db_connection():
    """Получение подключения к БД"""
    database_url = os.getenv("DATABASE_URL")
    connect = None
    try:
        connect = await asyncpg.connect(database_url)
        print("Успешное подключение к базе данных")
    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")
    return connect


@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    print("Execute cmd_start")

    if is_admin(message.from_user.id):
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text="📦 Последние заказы", callback_data="recent_orders"))
        keyboard.add(InlineKeyboardButton(text="📊 Статистика", callback_data="stats"))
        keyboard.add(InlineKeyboardButton(text="🛍️ Товары", callback_data="products"))

        await message.answer(
            "👋 Добро пожаловать в панель управления *AromaBay*!\n"
            "Здесь вы можете управлять заказами и отслеживать статистику магазина.",
            reply_markup=keyboard.as_markup(),
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            "👋 Привет! Я бот магазина *AromaBay*.\n"
            "Для доступа к панели управления обратитесь к администратору.",
            parse_mode="Markdown"
        )


@dp.message(Command("orders"))
async def cmd_orders(message: Message):
    """Показать последние заказы"""
    print("Execute cmd_orders")

    if not is_admin(message.from_user.id):
        print(message.from_user.id)
        await message.answer("❌ У вас нет доступа к этой команде.")
        return

    conn = await get_db_connection()
    try:
        orders = await conn.fetch(
            "SELECT * FROM orders ORDER BY created_at DESC LIMIT 5"
        )

        if not orders:
            await message.answer("📭 Заказов пока нет.")
            return

        response = "📦 *Последние заказы:*\n\n"
        for order in orders:
            status_emoji = "✅" if order['status'] == 'confirmed' else "⏳" if order['status'] == 'pending' else "❌"
            response += (
                f"{status_emoji} *Заказ #{order['id']}*\n"
                f"├ 👤 {order['user_name']}\n"
                f"├ 📧 {order['user_email']}\n"
                f"├ 💰 {order['total_amount']} руб\n"
                f"├ 📊 {order['status']}\n"
                f"└ 📅 {order['created_at'].strftime('%d.%m.%Y %H:%M')}\n\n"
            )

        # Создаем кнопки для управления заказами
        keyboard = InlineKeyboardBuilder()
        for order in orders:
            if order['status'] == 'pending':
                keyboard.add(InlineKeyboardButton(
                    text=f"✅ Подтвердить #{order['id']}",
                    callback_data=f"confirm_{order['id']}"
                ))

        if len(keyboard.buttons) > 0:
            keyboard.adjust(1)  # По одной кнопке в строке

        await message.answer(response, reply_markup=keyboard.as_markup(), parse_mode="Markdown")

    except Exception as e:
        await message.answer(f"❌ Ошибка при получении заказов: {str(e)}")
    finally:
        await conn.close()


@dp.message(Command("stats"))
async def cmd_stats(message: Message):
    """Показать статистику магазина"""
    print("Execute cmd_stats")

    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа к этой команде.")
        return

    conn = await get_db_connection()
    try:
        # Основная статистика
        total_orders = await conn.fetchval("SELECT COUNT(*) FROM orders")
        total_revenue = await conn.fetchval(
            "SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE status = 'confirmed'") or 0
        pending_orders = await conn.fetchval("SELECT COUNT(*) FROM orders WHERE status = 'pending'")
        confirmed_orders = await conn.fetchval("SELECT COUNT(*) FROM orders WHERE status = 'confirmed'")

        # Статистика по товарам
        total_products = await conn.fetchval("SELECT COUNT(*) FROM perfumes")
        low_stock_products = await conn.fetchval("SELECT COUNT(*) FROM perfumes WHERE stock_quantity < 10")

        stats_text = (
            "📊 *Статистика магазина*\n\n"
            f"🛍️ *Заказы:*\n"
            f"├ 📦 Всего: {total_orders}\n"
            f"├ ✅ Подтверждено: {confirmed_orders}\n"
            f"├ ⏳ Ожидают: {pending_orders}\n"
            f"└ 💰 Выручка: {total_revenue:.2f} руб\n\n"
            f"🏪 *Товары:*\n"
            f"├ 🛍️ Всего: {total_products}\n"
            f"└ ⚠️ Мало на складе: {low_stock_products}\n\n"
            f"_Обновлено: {message.date.strftime('%d.%m.%Y %H:%M')}_"
        )

        await message.answer(stats_text, parse_mode="Markdown")

    except Exception as e:
        await message.answer(f"❌ Ошибка при получении статистики: {str(e)}")
    finally:
        await conn.close()


@dp.callback_query(F.data == "recent_orders")
async def show_recent_orders(callback: types.CallbackQuery):
    """Показать последние заказы через callback"""
    print("Execute show_recent_orders")

    await cmd_orders(callback.message)
    await callback.answer()


@dp.callback_query(F.data == "stats")
async def show_stats(callback: types.CallbackQuery):
    """Показать статистику через callback"""
    print("Execute show_stats")

    await cmd_stats(callback.message)
    await callback.answer()


@dp.callback_query(F.data == "products")
async def show_products(callback: types.CallbackQuery):
    """Показать список товаров"""
    print("Execute show_products")

    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет доступа")
        return

    conn = await get_db_connection()
    try:
        products = await conn.fetch(
            "SELECT * FROM perfumes WHERE is_active = true ORDER BY name LIMIT 10"
        )

        if not products:
            await callback.message.answer("🛍️ Товаров пока нет в базе.")
            return

        response = "🛍️ *Товары в каталоге:*\n\n"
        for product in products:
            stock_emoji = "⚠️" if product['stock_quantity'] < 5 else "✅"
            response += (
                f"{stock_emoji} *{product['name']}*\n"
                f"├ 🏷️ {product['brand']}\n"
                f"├ 💰 {product['price']} руб\n"
                f"├ 📦 {product['stock_quantity']} шт.\n"
                f"└ 🏷️ {product['perfume_type']}\n\n"
            )

        await callback.message.edit_text(response, parse_mode="Markdown")

    except Exception as e:
        await callback.message.edit_text(f"❌ Ошибка при получении товаров: {str(e)}")
    finally:
        await conn.close()


@dp.callback_query(F.data.startswith("confirm_"))
async def confirm_order(callback: types.CallbackQuery):
    """Подтверждение заказа админом"""
    print("Execute confirm_order")
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет доступа")
        return

    order_id = int(callback.data.split("_")[1])
    print(f"order_id = {order_id}")
    conn = await get_db_connection()
    try:
        # Обновляем статус заказа
        result = await conn.execute(
            "UPDATE orders SET status = 'confirmed' WHERE id = $1 AND status = 'pending'",
            order_id
        )

        if "1" in result:  # Если обновлена 1 запись
            # Получаем информацию о заказе для уведомления
            order = await conn.fetchrow(
                "SELECT user_name, user_email, total_amount FROM orders WHERE id = $1",
                order_id
            )

            success_message = (
                f"✅ *Заказ #{order_id} подтвержден!*\n\n"
                f"👤 Клиент: {order['user_name']}\n"
                f"📧 Email: {order['user_email']}\n"
                f"💰 Сумма: {order['total_amount']} руб\n\n"
                f"_Заказ передан в отдел доставки_"
            )

            await callback.message.edit_text(success_message, parse_mode="Markdown")
            # Отправляем уведомление всем админам
            notification_message = (
                f"👨‍💼 *ЗАКАЗ ПОДТВЕРЖДЕН*\n"
                f"├ Номер: #{order_id}\n"
                f"├ Клиент: {order['user_name']}\n"
                f"└ Админ: {callback.from_user.first_name}\n"
                f"\n_Заказ готов к отправке_"
            )
            await send_to_admins(notification_message)

        else:
            await callback.answer("❌ Заказ не найден или уже обработан")
            
    except Exception as e:
        await callback.answer(f"❌ Ошибка: {str(e)}")
    finally:
        await conn.close()


@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Справка по командам"""
    print("Execute cmd_help")
    if is_admin(message.from_user.id):
        help_text = (
            "📖 *Доступные команды:*\n\n"
            "`/start` - Главное меню\n"
            "`/orders` - Последние заказы\n"
            "`/stats` - Статистика магазина\n"
            "`/help` - Эта справка\n\n"
            "*Управление заказами:*\n"
            "─ Используйте кнопки под сообщениями\n"
            "─ Подтверждайте заказы кнопкой '✅ Подтвердить'\n\n"
            "*Уведомления:*\n"
            "─ Вы будете получать уведомления о новых заказах\n"
            "─ И о проблемах с товарами"
        )
    else:
        help_text = (
            "👋 Я бот магазина *AromaBay*\n\n"
            "Для доступа к панели управления обратитесь к администратору."
        )

    await message.answer(help_text, parse_mode="Markdown")


async def start_bot():
    """Запуск бота"""
    print("🤖 Starting Telegram bot...")
    conn = await get_db_connection()
    await dp.start_polling(bot)