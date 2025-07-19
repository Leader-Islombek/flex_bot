import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from config import BOT_TOKEN, ADMIN_ID
from handlers import (
    start_handler, check_age,
    broadcast_handler, process_broadcast, Broadcast,
    contact_admin_handler, process_contact_admin, ContactAdmin
)
from database import get_users
from aiogram.fsm.storage.memory import MemoryStorage
from database import init_db

# Dastur boshida
init_db()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# --- /start komandasi ---
@dp.message(Command("start"))
async def start(message: Message):
    await start_handler(message)

# --- Flex haqida tugmasi ---
@dp.message(lambda message: message.text == "📖 Flex haqida")
async def flex_info(message: Message):
    text = """
🇺🇸 *FLEX nima?*

FLEX (Future Leaders Exchange) – AQSh hukumati tomonidan moliyalashtiriladigan dastur bo‘lib, o‘rta maktab o‘quvchilarini 1 yil davomida Amerika maktabida o‘qish va amerikalik oilada yashash imkonini beradi.

✅ Xarajatlar to‘liq qoplanadi  
✅ Ingliz tilini mukammal o‘rganish  
✅ Yetakchilik va madaniyat almashinuvi tajribasi

🔗 *Batafsil ma’lumot:* [Amerika Kengashlari FLEX bo‘limi](https://americancouncils.org.uz/flex)
"""
    await message.answer(text, parse_mode="Markdown")


# --- Yosh tekshirish tugmasi ---
@dp.message(lambda message: message.text == "📝 Yoshni tekshirish")
async def flex_check(message: Message):
    await message.answer("🗓 Tug‘ilgan sanangizni kiriting (YYYY-MM-DD) masalan 2009-05-15:")

# --- Admin'ga xabar tugmasi ---
@dp.message(lambda message: message.text == "✉️ Admin'ga xabar")
async def contact_admin_btn(message: Message, state):
    await contact_admin_handler(message, state)

# --- Admin panel tugmasi ---
@dp.message(lambda message: message.text == "👤 Admin panel" and message.from_user.id == ADMIN_ID)
async def admin_panel(message: Message):
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👥 Userlar ro‘yxati")],
            [KeyboardButton(text="✉️ Broadcast")],
            [KeyboardButton(text="📊 Statistika")],
            [KeyboardButton(text="🔙 Ortga")]
        ],
        resize_keyboard=True
    )
    await message.answer("👤 *Admin panel*\n\nKerakli bo‘limni tanlang:", reply_markup=keyboard, parse_mode="Markdown")

# --- Ortga tugmasi ---
@dp.message(lambda message: message.text == "🔙 Ortga" and message.from_user.id == ADMIN_ID)
async def back_to_main(message: Message):
    await start_handler(message)

# --- Userlar ro‘yxati ---
@dp.message(lambda message: message.text == "👥 Userlar ro‘yxati" and message.from_user.id == ADMIN_ID)
async def user_list(message: Message):
    users = get_users()
    if not users:
        await message.answer("🚫 Hech qanday foydalanuvchi topilmadi.")
        return

    text = "👥 *Bot foydalanuvchilari:*\n\n"
    for idx, u in enumerate(users, 1):
        user_id = u[1]
        text += f"{idx}. [{user_id}](tg://user?id={user_id})\n"

    await message.answer(text, parse_mode="Markdown")

# --- Statistika ---
@dp.message(lambda message: message.text == "📊 Statistika" and message.from_user.id == ADMIN_ID)
async def stats(message: Message):
    users = get_users()
    total_users = len(users)

    await message.answer(f"📊 *Bot statistikasi:*\n\n👥 Jami foydalanuvchilar: {total_users}", parse_mode="Markdown")

# --- Broadcast tugmasi ---
@dp.message(lambda message: message.text == "✉️ Broadcast" and message.from_user.id == ADMIN_ID)
async def broadcast_btn(message: Message, state):
    await broadcast_handler(message, state)

# --- Broadcast process ---
@dp.message(Broadcast.waiting_message)
async def process_broadcast_message(message: Message, state):
    await process_broadcast(message, state, bot)

# --- Contact admin process ---
@dp.message(ContactAdmin.waiting_message)
async def process_contact_admin_message(message: Message, state):
    await process_contact_admin(message, state, bot)

# --- Tugilgan sana yoki umumiy matnlar handleri ---
@dp.message()
async def handle_birthdate_or_text(message: Message, state):
    current_state = await state.get_state()
    
    # Admin panel tugmalarini umumiy handlerdan chiqarish
    if message.from_user.id == ADMIN_ID and message.text in [
        "👥 Userlar ro‘yxati",
        "✉️ Broadcast",
        "📊 Statistika",
        "🔙 Ortga",
        "👤 Admin panel"
    ]:
        return  # bu tugmalar alohida handlerlar tomonidan ishlatiladi

    if current_state == ContactAdmin.waiting_message:
        await process_contact_admin(message, state, bot)
    elif current_state == Broadcast.waiting_message:
        await process_broadcast(message, state, bot)
    else:
        await check_age(message)

# --- Botni ishga tushirish ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
