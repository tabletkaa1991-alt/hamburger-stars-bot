import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0") or 0)

YUKASSA_SHOP_ID = os.getenv("YUKASSA_SHOP_ID", "")
YUKASSA_SECRET = os.getenv("YUKASSA_SECRET", "")
RETURN_URL = os.getenv("RETURN_URL", "https://t.me/Hamburger_Stars_bot")

FRAGMENT_SESSION = os.getenv("FRAGMENT_SESSION", "")
FRAGMENT_PAYMENT = os.getenv("FRAGMENT_PAYMENT", "TON")

DB_PATH = BASE_DIR / "data" / "orders.db"
