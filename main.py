import asyncio
import logging
from aiogram import types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from config import ADMIN_ID
from database import database
from bot import bot, dp
from handlers import (
    Broadcast,
    ContactAdmin,
    start_handler,
    flex_info,
    ask_birthdate,
    check_age,
    admin_panel,
    user_list,
    stats,
    broadcast_handler,
    process_broadcast,
    contact_admin_handler,
    process_contact_admin,
    back_to_main,
    handle_other_messages,
    stop_bot,
)
from aiogram.fsm.state import State, StatesGroup

# --- Configure logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)


# --- Register all handlers ---

# Command handlers
dp.message.register(start_handler, Command("start"))
dp.message.register(stop_bot, Command("stopbot"))

# Text message handlers
dp.message.register(flex_info, lambda message: message.text == "📖 Flex haqida")
dp.message.register(ask_birthdate, lambda message: message.text == "📝 Yoshni tekshirish")
dp.message.register(admin_panel, lambda message: message.text == "👤 Admin panel" and message.from_user.id == ADMIN_ID)
dp.message.register(user_list, lambda message: message.text == "👥 Userlar ro'yxati" and message.from_user.id == ADMIN_ID)
dp.message.register(stats, lambda message: message.text == "📊 Statistika" and message.from_user.id == ADMIN_ID)
dp.message.register(broadcast_handler, lambda message: message.text == "✉️ Broadcast" and message.from_user.id == ADMIN_ID)
dp.message.register(contact_admin_handler, lambda message: message.text == "✉️ Admin'ga xabar")
dp.message.register(back_to_main, lambda message: message.text == "🔙 Ortga" and message.from_user.id == ADMIN_ID)

# Yangiliklar kanali
@dp.message(lambda message: message.text == "🔔 Yangiliklar kanali")
async def send_channel_link(message: Message):
    await message.answer("🇺🇸 FLEX yangiliklar kanalimizga qo‘shiling:\nhttps://t.me/flexuzbinfo")

# Special handlers
dp.message.register(check_age, lambda message: message.text and len(message.text.split('-')) == 3)
dp.message.register(process_broadcast, Broadcast.waiting_message)
dp.message.register(process_contact_admin, ContactAdmin.waiting_message)

# Cancel handler
@dp.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🚫 Amal bekor qilindi.")

# Default handler
dp.message.register(handle_other_messages)


# --- Lifecycle events ---
async def on_startup():
    logger.info("🔄 Bot ishga tushmoqda...")
    try:
        await database.connect()
        logger.info("✅ Database ulandi.")
    except Exception as e:
        logger.error(f"❌ Database ulanishida xatolik: {e}")
    await bot.send_message(ADMIN_ID, "🤖 Bot ishga tushdi")


async def on_shutdown():
    logger.info("🔻 Bot to'xtamoqda...")
    await database.disconnect()
    await bot.send_message(ADMIN_ID, "🤖 Bot to'xtatildi")


# --- Main function ---
async def main():
    await on_startup()
    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("🚨 Bot to'xtatildi (KeyboardInterrupt yoki SystemExit)")
