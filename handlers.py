import sys
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from datetime import datetime
from bot import bot 
from database import get_users, add_user_if_not_exists, get_user_count
from config import ADMIN_ID
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils import calculate_age

# --- States ---
class Broadcast(StatesGroup):
    waiting_message = State()

class ContactAdmin(StatesGroup):
    waiting_message = State()

# --- /start handler ---
async def start_handler(message: types.Message):
    user = message.from_user
    added = await add_user_if_not_exists(  # ✅ await qo‘shildi
        tg_id=user.id, # type: ignore
        full_name=user.full_name, # type: ignore
        birth_date=None,
        username=user.username # type: ignore
    )

    user_buttons = [
        [KeyboardButton(text="📖 Flex haqida")],
        [KeyboardButton(text="📝 Yoshni tekshirish")],
        [KeyboardButton(text="✉️ Admin'ga xabar")],
        [KeyboardButton(text="🔔 Yangiliklar kanali")]
    ]

    if user.id == ADMIN_ID: # type: ignore
        user_buttons.append([KeyboardButton(text="👤 Admin panel")])

    keyboard = ReplyKeyboardMarkup(
        keyboard=user_buttons,
        resize_keyboard=True
    )

    welcome_text = "👋 Assalomu alaykum!\n\nBotga xush kelibsiz."
    if added:
        welcome_text += "\n\n✅ Siz ro'yxatga olindingiz."
    
    await message.answer(welcome_text, reply_markup=keyboard)


# --- Flex haqida info ---
async def flex_info(message: types.Message):
    text = """
🇺🇸 *FLEX nima?*

FLEX (Future Leaders Exchange) - AQSh hukumati tomonidan moliyalashtiriladigan dastur bo'lib, o'rta maktab o'quvchilarini yani 9-10 sinflarni 1 yil davomida Amerika maktabida o'qish va amerikalik oilada yashash imkonini beradi.
Nimalar bo'ladi?
✅ 1 yil davomida AQShda o'qish
✅ Xarajatlar to'liq qoplanadi  
✅ Ingliz tilini mukammal o'rganish  
✅ Yetakchilik va madaniyat almashinuvi tajribasi

🔗 *Batafsil ma'lumot:* [Amerika Kengashlari FLEX bo'limi](https://www.discoverflex.org/)
"""
    await message.answer(text, parse_mode="Markdown")


# --- Yosh tekshirish so'rovi ---
async def ask_birthdate(message: types.Message):
    await message.answer("🗓 Tug'ilgan sanangizni kiriting (YYYY-MM-DD) masalan 2009-05-15:")


# --- Yoshni hisoblash ---
async def check_age(message: types.Message):
    from database import update_birth_date  # ⚠️ import qil

    try:
        birthdate = datetime.strptime(message.text, "%Y-%m-%d") # type: ignore
    except ValueError:
        await message.answer("❌ Noto'g'ri format. Iltimos, YYYY-MM-DD formatida kiriting.")
        return

    # 🔥 Tug‘ilgan sanani bazaga saqlaymiz
    await update_birth_date(message.from_user.id, message.text)  # type: ignore

    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    total_months = (today.year - birthdate.year) * 12 + today.month - birthdate.month

    flex_check_date = datetime(2026, 8, 1)
    flex_age = flex_check_date.year - birthdate.year - ((flex_check_date.month, flex_check_date.day) < (birthdate.month, birthdate.day))

    if flex_age < 15:
        result = "❌ Afsuski, FLEX uchun yoshingiz juda kichik."
    elif flex_age > 17:
        result = "❌ Afsuski, FLEX uchun yoshingiz juda katta."
    else:
        result = "✅ Tabriklaymiz! Siz FLEX uchun yosh talabiga mos kelasiz."

    response = f"""
📅 Tug'ilgan sana: {birthdate.strftime('%Y-%m-%d')}
🔢 Yosh: {age}
🗓 O'tgan oylar: {total_months}

🎯 FLEX tekshirish natijasi:
{result}
"""
    await message.answer(response)



# --- Admin panel ---
async def admin_panel(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👥 Userlar ro'yxati")],
            [KeyboardButton(text="✉️ Broadcast")],
            [KeyboardButton(text="📊 Statistika")],
            [KeyboardButton(text="🔙 Ortga")]
        ],
        resize_keyboard=True
    )
    await message.answer("👤 *Admin panel*\n\nKerakli bo'limni tanlang:", reply_markup=keyboard, parse_mode="Markdown")


# --- Botni to‘xtatish komandasi ---
async def stop_bot(message: types.Message):
    if message.from_user.id == ADMIN_ID: # type: ignore
        await message.answer("🛑 Bot to‘xtatilmoqda...")
        await bot.session.close()
        sys.exit()
    else:
        await message.answer("❌ Siz admin emassiz.")


# --- Userlar ro'yxati ---
async def user_list(message: types.Message):
    users = await get_users()
    if not users:
        await message.answer("🚫 Hech qanday foydalanuvchi topilmadi.")
        return

    text = "👥 <b>Bot foydalanuvchilari:</b>\n\n"
    for idx, user in enumerate(users, 1):
        user_id = user[1]
        full_name = user[2]
        birth_date = user[3]
        username = f"@{user[5]}" if user[5] else "Yo'q"
        join_date = user[4]

        if birth_date:
            try:
                age = calculate_age(birth_date)
            except:
                age = "Xato"
        else:
            age = "Noma'lum"

        text += (
            f"{idx}. <b>ID:</b> {user_id}\n"
            f"   <b>Ism:</b> {full_name}\n"
            f"   <b>Username:</b> {username}\n"
            f"   <b>Yosh:</b> {age}\n"
            f"   <b>Qo'shilgan:</b> {join_date}\n\n"
        )

    await message.answer(text, parse_mode="HTML")


# --- Broadcast ---
async def broadcast_handler(message: types.Message, state: FSMContext):
    await message.answer("✉️ Yuboriladigan xabar matnini yozing:")
    await state.set_state(Broadcast.waiting_message)


async def process_broadcast(message: types.Message, state: FSMContext):
    users = await get_users()
    if not users:
        await message.answer("⚠️ Bazada foydalanuvchilar topilmadi!")
        await state.clear()
        return

    success = 0
    for user in users:
        try:
            await message.bot.send_message(user[1], message.text) # type: ignore
            success += 1
        except Exception as e:
            print(f"Xatolik user {user[1]}ga xabar yuborishda: {e}")

    await message.answer(f"✅ Xabar {success}/{len(users)} ta foydalanuvchiga yuborildi.")
    await state.clear()


# --- Statistika ---
async def stats(message: types.Message):
    count = await get_user_count()
    await message.answer(f"📊 *Bot statistikasi:*\n\n👥 Jami foydalanuvchilar: {count}", parse_mode="Markdown")


# --- Admin'ga xabar ---
async def contact_admin_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID: # type: ignore
        await message.answer("❌ Siz adminsiz, o'zingizga xabar yuborolmaysiz!")
        return
    
    await message.answer(
        "✍️ Admin'ga yubormoqchi bo'lgan xabaringizni yozing:\n"
        "⚠️ Xabar matni 10 belgidan kam bo'lmasligi kerak!\n"
        "🚫 Bekor qilish uchun /cancel buyrug'ini yuboring"
    )
    await state.set_state(ContactAdmin.waiting_message)


async def process_contact_admin(message: types.Message, state: FSMContext):
    if len(message.text.strip()) < 10: # type: ignore
        await message.answer("❌ Xabar juda qisqa! Kamida 10 belgi bo'lishi kerak.")
        return
    
    if message.text == "/cancel":
        await state.clear()
        await message.answer("✅ Xabar yuborish bekor qilindi.")
        return
    
    try:
        user_info = (
            f"👤 Foydalanuvchi: {message.from_user.full_name}\n" # type: ignore
            f"🆔 ID: {message.from_user.id}\n" # type: ignore
        )
        if message.from_user.username: # type: ignore
            user_info += f"📎 @{message.from_user.username}\n" # type: ignore
        
        admin_message = (
            f"📨 Yangi xabar:\n\n"
            f"{user_info}\n"
            f"📝 Xabar matni:\n"
            f"{message.text}"
        )
        
        await message.bot.send_message(chat_id=ADMIN_ID, text=admin_message) # type: ignore
        await message.answer("✅ Xabaringiz admin'ga muvaffaqiyatli yuborildi!")
        
    except Exception as e:
        await message.answer("❌ Xabar yuborishda xatolik yuz berdi. Iltimos, keyinroq urunib ko'ring.")
        print(f"Xatolik admin'ga xabar yuborishda: {e}")
    finally:
        await state.clear()


# --- Ortga ---
async def back_to_main(message: types.Message):
    await start_handler(message)


# --- Boshqa xabarlar uchun handler ---
async def handle_other_messages(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    
    if current_state == ContactAdmin.waiting_message:
        await process_contact_admin(message, state)
    elif current_state == Broadcast.waiting_message:
        await process_broadcast(message, state)
    else:
        await message.answer("Iltimos, menyudan biror tugmani tanlang yoki /start buyrug'ini yuboring")
