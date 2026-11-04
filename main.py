import asyncio
import os

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

import config
from bot import router
from db import init_db

WEBHOOK_PATH = "/webhook"


async def main():
    init_db()
    bot = Bot(config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    base_url = os.getenv("RENDER_EXTERNAL_URL", "").rstrip("/")
    if base_url:
        await bot.set_webhook(base_url + WEBHOOK_PATH)

    app = web.Application()
    app.router.add_get("/", lambda r: web.Response(text="ok"))
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))


if __name__ == "__main__":
    asyncio.run(main())
