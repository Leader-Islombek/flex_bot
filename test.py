from database import add_user, get_user, log_message

# Yangi foydalanuvchi qo'shish
add_user(12345, "John Doe", "2000-05-15", "johndoe")

# Foydalanuvchi ma'lumotlarini olish
user = get_user(12345)
print(user)

# Xabar log qilish
log_message(12345, "Salom, bu test xabari!")