import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if ADMIN_ID is None:
    raise ValueError("ADMIN_ID environment variable not set.")
else:
    ADMIN_ID = int(ADMIN_ID)
