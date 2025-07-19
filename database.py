import sqlite3

def connect_db():
    conn = sqlite3.connect("flex.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            tg_id INTEGER,
            fullname TEXT,
            birthdate TEXT,
            join_date TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            tg_id INTEGER,
            message TEXT,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_user(tg_id, fullname, birthdate, join_date):
    conn = sqlite3.connect("flex.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO users (tg_id, fullname, birthdate, join_date) VALUES (?, ?, ?, ?)",
                (tg_id, fullname, birthdate, join_date))
    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect("flex.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    conn.close()
    return users

def log_message(tg_id, message, date):
    conn = sqlite3.connect("flex.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (tg_id, message, date) VALUES (?, ?, ?)",
                (tg_id, message, date))
    conn.commit()
    conn.close()

def get_messages():
    conn = sqlite3.connect("flex.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages")
    messages = cur.fetchall()
    conn.close()
    return messages

def delete_user(tg_id):
    conn = sqlite3.connect("flex.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE tg_id = ?", (tg_id,))
    conn.commit()
    conn.close()
    
def get_messages_count():
    conn = sqlite3.connect("flex.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM messages")
    count = cur.fetchone()[0]
    conn.close()
    return count

def get_top_user():
    conn = sqlite3.connect("flex.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT tg_id, COUNT(*) as total FROM messages
        GROUP BY tg_id
        ORDER BY total DESC
        LIMIT 1
    """)
    result = cur.fetchone()
    conn.close()
    return result

def init_db():
    """Baza faylini va jadvallarni yaratish uchun"""
    print("Baza ishga tushirilmoqda...")
    try:
        connect_db()  # Bu sizning mavjud connect_db funksiyangiz
        print("✅ Baza muvaffaqiyatli ishga tushirildi")
        return True
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        return False