from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN

# Bot instance with default parse_mode
bot = Bot(
    token=BOT_TOKEN, # type: ignore
    default=DefaultBotProperties(parse_mode="HTML")
)

# Dispatcher instance
dp = Dispatcher(storage=MemoryStorage())
