# ✔️ FlexUzbBot

**FLEX Uzbekistan Telegram bot**

---

## 📌 **Bot nima qiladi?**

✅ Future Leaders Exchange (FLEX) dasturi haqida to‘liq ma’lumot beradi  
✅ Topshiruvchi o‘quvchilar yoshining mosligini tekshiradi  
✅ Admin panel orqali userlarni ko‘rish, broadcast yuborish va statistika olish imkonini beradi

---

## 🚀 **Features**

- /start – Botni boshlash
- 📖 FLEX haqida – FLEX dasturi haqida umumiy tushuntirish
- 🎂 Yosh tekshirish – tug‘ilgan sanaga qarab eligibility tekshiradi
- 👤 Admin panel – user ro‘yxati, broadcast, statistika
- Inline tugmalar orqali qulay interfeys
- SQLite database bilan user management
- Railway’da online deploy qilingan

---

## ⚙️ **Texnologiyalar**

- **Python 3.11+**
- **Aiogram 3**
- **SQLite3**
- **Railway deploy**

---

## 🔧 **Loyihani ishga tushirish**

1. **Clone project**

```bash
git clone https://github.com/Leader-Islombek/flex_bot.git
cd flex_bot

python -m venv venv
source venv/bin/activate  # MacOS/Linux
venv\Scripts\activate     # Windows

pip install -r requirements.txt

.env:
BOT_TOKEN=your_telegram_bot_token
ADMIN_ID=your_telegram_user_id

python
>>> from database import init_db
>>> init_db()
>>> exit()

python main.py

🛠 Deployment (Railway)
1. Railway account yarat
2. GitHub repo ulash
3. Environment variables qo‘y:
   BOT_TOKEN
   ADMIN_ID
4. Deploy bos ➔ bot online bo‘ladi
## Privacy Policy
📝 Privacy Policy
This bot does not collect or store any personal data except date of birth for FLEX eligibility check. Your data will not be shared with third parties.

👨🏻‍💻 Author
Islombek – Future Leaders Developer

Telegram | GitHub
