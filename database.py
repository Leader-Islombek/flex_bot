import sqlite3

def connect_db():
    """Bazaga ulanish va jadvallarni yaratish"""
    conn = sqlite3.connect("flex.db")
    cur = conn.cursor()
    
    # Users jadvalini yaratish (AUTOINCREMENT qo'shildi)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER UNIQUE,
        fullname TEXT,
        birthdate TEXT,
        join_date TEXT
    )
    """)
    
    # Messages jadvalini yaratish (FOREIGN KEY qo'shildi)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER,
        message TEXT,
        date TEXT,
        FOREIGN KEY (tg_id) REFERENCES users(tg_id)
    )
    """)
    
    conn.commit()
    return conn
import os

def init_db():
    """Baza fayli va jadvallarni ishga tushirish"""
    # Baza faylini tekshirish va yaratish
    if not os.path.exists('flex.db'):
        open('flex.db', 'w').close()
    
    with sqlite3.connect('flex.db') as conn:
        cur = conn.cursor()
        
        # Users jadvalini yaratish
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER UNIQUE,
            fullname TEXT,
            birthdate TEXT,
            join_date TEXT
        )
        """)
        
        # Messages jadvalini yaratish
        cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER,
            message TEXT,
            date TEXT
        )
        """)
        
        conn.commit()

# Dastur ishga tushganda baza yaratilishini ta'minlash
init_db()

def add_user(tg_id, fullname, birthdate, join_date):
    conn = sqlite3.connect("flex.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO users (tg_id, fullname, birthdate, join_date) VALUES (?, ?, ?, ?)",
                (tg_id, fullname, birthdate, join_date))
    conn.commit()
    conn.close()

def get_users():
    """Barcha foydalanuvchilarni olish"""
    init_db()  # Jadval mavjudligini qo'shimcha tekshirish
    with sqlite3.connect('flex.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        return cur.fetchall()

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
