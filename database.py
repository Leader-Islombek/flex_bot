import sqlite3
import os
from datetime import datetime
from pathlib import Path

# Database file path
DB_PATH = Path("flex.db")

def connect_db():
    """Create and return a database connection"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """Initialize database tables"""
    with connect_db() as conn:
        cur = conn.cursor()
        
        # Users table
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
        
        # Messages table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER NOT NULL,
            message_text TEXT NOT NULL,
            sent_date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tg_id) REFERENCES users(tg_id)
        )
        """)
        
        # Create indexes
        cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_users_tg_id ON users(tg_id)
        """)
        
        cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_messages_tg_id ON messages(tg_id)
        """)
        
        conn.commit()

def add_user_if_not_exists(tg_id, full_name, birth_date=None, username=None):
    """Add user if not exists in database"""
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO users (tg_id, full_name, birth_date, username) VALUES (?, ?, ?, ?)",
            (tg_id, full_name, birth_date, username)
        )
        conn.commit()
        return cur.rowcount > 0

def get_users():
    """Get all users from database"""
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users ORDER BY join_date DESC")
        return cur.fetchall()

def get_user_count():
    """Get total number of users"""
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users")
        return cur.fetchone()[0]

def log_message(tg_id, message_text):
    """Log a message to database"""
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO messages (tg_id, message_text) VALUES (?, ?)",
            (tg_id, message_text)
        )
        conn.commit()
        return cur.lastrowid

# Initialize database when module is imported
init_db()