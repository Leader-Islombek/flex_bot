import asyncio
import logging
from tkinter import Message
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from config import BOT_TOKEN, ADMIN_ID
from database import init_db
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
    handle_other_messages
)
from aiogram.fsm.state import State, StatesGroup

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database
init_db()

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# --- Register all handlers ---

# Command handlers
dp.message.register(start_handler, Command("start"))

# Text message handlers
dp.message.register(flex_info, lambda message: message.text == "📖 Flex haqida")
dp.message.register(ask_birthdate, lambda message: message.text == "📝 Yoshni tekshirish")
dp.message.register(admin_panel, lambda message: message.text == "👤 Admin panel" and message.from_user.id == ADMIN_ID)
dp.message.register(user_list, lambda message: message.text == "👥 Userlar ro'yxati" and message.from_user.id == ADMIN_ID)
dp.message.register(stats, lambda message: message.text == "📊 Statistika" and message.from_user.id == ADMIN_ID)
dp.message.register(broadcast_handler, lambda message: message.text == "✉️ Broadcast" and message.from_user.id == ADMIN_ID)
dp.message.register(contact_admin_handler, lambda message: message.text == "✉️ Admin'ga xabar")
dp.message.register(back_to_main, lambda message: message.text == "🔙 Ortga" and message.from_user.id == ADMIN_ID)

# Special handlers
dp.message.register(check_age, lambda message: message.text and len(message.text.split('-')) == 3)
dp.message.register(process_broadcast, Broadcast.waiting_message)
dp.message.register(process_contact_admin, ContactAdmin.waiting_message)

@dp.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🚫 Amal bekor qilindi.")
    
# Default handler
dp.message.register(handle_other_messages)

async def on_startup():
    """Bot ishga tushganda"""
    logger.info("Bot ishga tushmoqda...")
    await bot.send_message(ADMIN_ID, "🤖 Bot ishga tushdi")

async def on_shutdown():
    """Bot to'xtaganda"""
    logger.info("Bot to'xtamoqda...")
    await bot.send_message(ADMIN_ID, "🤖 Bot to'xtadi")

async def main():
    await on_startup()
    await dp.start_polling(bot)
    await on_shutdown()

if __name__ == "__main__":
    asyncio.run(main())