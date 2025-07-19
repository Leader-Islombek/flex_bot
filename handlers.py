from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from datetime import datetime
from database import get_users, add_user
from config import ADMIN_ID
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import sqlite3
# --- States ---
class Broadcast(StatesGroup):
    waiting_message = State()

class ContactAdmin(StatesGroup):
    waiting_message = State()

# --- /start handler ---
async def start_handler(message: types.Message):
    user = message.from_user
    
    # Foydalanuvchini bazaga qo'shamiz
    added = add_user(
        tg_id=user.id,
        fullname=user.full_name,
        birthdate=None  # Keyinroq to'ldiriladi
    )
    
    # Oddiy user tugmalari
    user_buttons = [
        [KeyboardButton(text="📖 Flex haqida")],
        [KeyboardButton(text="📝 Yoshni tekshirish")],
        [KeyboardButton(text="✉️ Admin'ga xabar")]
    ]

    # Agar admin bo‘lsa, admin panel tugmasini qo‘sh
    if message.from_user.id == ADMIN_ID:
        user_buttons.append([KeyboardButton(text="👤 Admin panel")])

    keyboard = ReplyKeyboardMarkup(
        keyboard=user_buttons,
        resize_keyboard=True
    )

    await message.answer(
        "👋 Assalomu alaykum!\n\nBotga xush kelibsiz.\nFlex haqida bilish uchun tugmalarni bosing.",
        reply_markup=keyboard
    )

@dp.message_handler(commands=['dbstatus'])
async def db_status(message: types.Message):
    with sqlite3.connect('flex.db') as conn:
        cur = conn.cursor()
        
        # Jadval mavjudligi
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cur.fetchall()]
        
        # Foydalanuvchilar soni
        cur.execute("SELECT COUNT(*) FROM users")
        user_count = cur.fetchone()[0]
        
        await message.answer(
            f"📊 Database status:\n"
            f"Jadvallar: {', '.join(tables) or 'Yoʻq'}\n"
            f"Foydalanuvchilar: {user_count}\n"
            f"Admin ID: {ADMIN_ID}"
        )

# --- FLEX yosh tekshirish funksiyasi ---
async def check_age(message: types.Message):
    try:
        birthdate = datetime.strptime(message.text, "%Y-%m-%d")
    except:
        await message.answer("❌ Tug‘ilgan sanani YYYY-MM-DD formatida yozing.")
        return

    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    total_months = (today.year - birthdate.year) * 12 + today.month - birthdate.month

    # FLEX uchun tekshirayotgan yil: 2026
    check_date = datetime(2026, 8, 1)
    flex_age = check_date.year - birthdate.year - ((check_date.month, check_date.day) < (birthdate.month, birthdate.day))

    # Sentabr cutoff
    cutoff_date = datetime(2008, 9, 1)

    # FLEX eligibility tekshirish
    if birthdate < cutoff_date:
        flex_result = "❌ Afsuski, FLEX uchun yoshingiz mos emas (2008-yil sentabrdan oldin tug‘ilgansiz)."
    elif flex_age < 15:
        flex_result = "❌ Afsuski, FLEX uchun yoshingiz juda kichik."
    elif flex_age > 17:
        flex_result = "❌ Afsuski, FLEX uchun yoshingiz juda katta."
    else:
        flex_result = "✅ Tabriklaymiz! Siz FLEX uchun yosh talabiga mos kelasiz."

    text = f"""
📅 Tug‘ilgan sana: {birthdate.strftime('%Y-%m-%d')}
🔢 Yosh: {age}
🗓 O‘tgan oylar: {total_months}

🎯 FLEX tekshirish natijasi:
{flex_result}
"""
    await message.answer(text)

# --- Admin broadcast boshlash handler ---
async def broadcast_handler(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Siz admin emassiz.")
        return

    await message.answer("✉️ Yuboriladigan xabar matnini yozing:")
    await state.set_state(Broadcast.waiting_message)

# --- Admin broadcast process handler ---
async def process_broadcast(message: types.Message, state: FSMContext, bot):
    users = get_users()
    success = 0

    for u in users:
        try:
            await bot.send_message(u[1], message.text)
            success += 1
        except:
            continue

    await message.answer(f"✅ Xabar {success} ta foydalanuvchiga yuborildi.")
    await state.clear()

# --- Userdan admin'ga xabar boshlash handler ---
async def contact_admin_handler(message: types.Message, state: FSMContext):
    await message.answer("✉️ Admin'ga yuboriladigan xabar matnini yozing:")
    await state.set_state(ContactAdmin.waiting_message)

# --- Userdan admin'ga xabar process handler ---
async def process_contact_admin(message: types.Message, state: FSMContext, bot):
    admin_id = ADMIN_ID
    text = f"📨 *Yangi xabar userdan:*\n\n"
    text += f"👤 [{message.from_user.full_name}](tg://user?id={message.from_user.id})\n"
    if message.from_user.username:
        text += f"🔗 @{message.from_user.username}\n"
    text += f"\n💬 {message.text}"

    await bot.send_message(admin_id, text, parse_mode="Markdown")
    await message.answer("✅ Xabaringiz admin'ga yuborildi.")
    await state.clear()
