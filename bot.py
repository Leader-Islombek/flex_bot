from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN

# Bot instance
bot = Bot(token=BOT_TOKEN, parse_mode="HTML") # type: ignore

# Dispatcher instance with memory storage (simple FSM)
dp = Dispatcher(storage=MemoryStorage())
