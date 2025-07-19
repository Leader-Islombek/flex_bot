import sqlite3
import os
from pathlib import Path
from datetime import datetime

# Baza fayli uchun doimiy joylashuv
DB_PATH = Path("flex.db")

def connect_db():
    """Bazaga ulanishni o'rnatish"""
    # Baza fayli va papkani yaratish
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """Baza strukturasini ishga tushirish"""
    with connect_db() as conn:
        cur = conn.cursor()
        
        # Users jadvali
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            birth_date TEXT,
            join_date TEXT DEFAULT CURRENT_TIMESTAMP,
            username TEXT
        )
        """)
        
        # Messages jadvali
        cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER NOT NULL,
            message_text TEXT NOT NULL,
            sent_date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tg_id) REFERENCES users (tg_id)
        )
        """)
        
        # Indexlar
        cur.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON users(tg_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_msg_user_id ON messages(tg_id)")
        
        conn.commit()

def add_user(tg_id, full_name, birth_date=None, username=None):
    """Yangi foydalanuvchi qo'shish"""
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO users (tg_id, full_name, birth_date, username) VALUES (?, ?, ?, ?)",
            (tg_id, full_name, birth_date, username)
        )
        conn.commit()
        return cur.lastrowid

def get_user(tg_id):
    """Foydalanuvchi ma'lumotlarini olish"""
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,))
        return cur.fetchone()

def get_all_users():
    """Barcha foydalanuvchilar ro'yxati"""
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users ORDER BY join_date DESC")
        return cur.fetchall()

def update_user(tg_id, full_name=None, birth_date=None, username=None):
    """Foydalanuvchi ma'lumotlarini yangilash"""
    with connect_db() as conn:
        cur = conn.cursor()
        updates = []
        params = []
        
        if full_name:
            updates.append("full_name = ?")
            params.append(full_name)
        if birth_date:
            updates.append("birth_date = ?")
            params.append(birth_date)
        if username:
            updates.append("username = ?")
            params.append(username)
            
        if updates:
            params.append(tg_id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE tg_id = ?"
            cur.execute(query, params)
            conn.commit()
            return cur.rowcount
        return 0

def delete_user(tg_id):
    """Foydalanuvchini o'chirish"""
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE tg_id = ?", (tg_id,))
        conn.commit()
        return cur.rowcount

def log_message(tg_id, message_text):
    """Xabarlarni log qilish"""
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO messages (tg_id, message_text) VALUES (?, ?)",
            (tg_id, message_text)
        )
        conn.commit()
        return cur.lastrowid

def get_user_messages(tg_id, limit=10):
    """Foydalanuvchi xabarlarini olish"""
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM messages WHERE tg_id = ? ORDER BY sent_date DESC LIMIT ?",
            (tg_id, limit)
        )
        return cur.fetchall()

def get_message_count():
    """Jami xabarlar soni"""
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM messages")
        return cur.fetchone()[0]

def get_top_active_users(limit=5):
    """Eng faol foydalanuvchilar"""
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT u.tg_id, u.full_name, COUNT(m.id) as message_count
            FROM users u
            LEFT JOIN messages m ON u.tg_id = m.tg_id
            GROUP BY u.tg_id
            ORDER BY message_count DESC
            LIMIT ?
        """, (limit,))
        return cur.fetchall()

def get_user_count():
    """Jami foydalanuvchilar soni"""
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users")
        return cur.fetchone()[0]

def calculate_age(tg_id):
    """Foydalanuvchi yoshini hisoblash"""
    user = get_user(tg_id)
    if not user or not user[3]:  # birth_date mavjud emas
        return None
    
    birth_date = datetime.strptime(user[3], "%Y-%m-%d")
    today = datetime.now()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

# Dastur ishga tushganda baza strukturasini tekshirish
init_db()