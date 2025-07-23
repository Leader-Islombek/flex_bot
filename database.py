import os
from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, ForeignKey, Index, func
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

database = Database(DATABASE_URL) # type: ignore
metadata = MetaData()

# Users table
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("tg_id", Integer, unique=True, nullable=False),
    Column("full_name", String, nullable=False),
    Column("birth_date", String),
    Column("join_date", DateTime, server_default=func.now()),
    Column("username", String)
)

# Messages table
messages = Table(
    "messages",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("tg_id", Integer, ForeignKey("users.tg_id"), nullable=False),
    Column("message_text", String, nullable=False),
    Column("sent_date", DateTime, server_default=func.now())
)

# Indexes
Index("idx_users_tg_id", users.c.tg_id)
Index("idx_messages_tg_id", messages.c.tg_id)

# Create engine and tables
engine = create_engine(DATABASE_URL) # type: ignore
metadata.create_all(engine)

# Add user if not exists
async def add_user_if_not_exists(tg_id, full_name, birth_date=None, username=None):
    query = users.select().where(users.c.tg_id == tg_id)
    existing_user = await database.fetch_one(query)
    if not existing_user:
        insert_query = users.insert().values(
            tg_id=tg_id,
            full_name=full_name,
            birth_date=birth_date,
            username=username
        )
        await database.execute(insert_query)
        return True
    return False

# Get all users
async def get_users():
    query = users.select().order_by(users.c.join_date.desc())
    return await database.fetch_all(query)

# Get user count
async def get_user_count():
    query = users.count() # type: ignore
    return await database.fetch_val(query)

# Log message
async def log_message(tg_id, message_text):
    insert_query = messages.insert().values(
        tg_id=tg_id,
        message_text=message_text
    )
    return await database.execute(insert_query)
