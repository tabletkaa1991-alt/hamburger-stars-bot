import asyncio
import os

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

import config
import payments
from bot import router
from db import init_db

WEBHOOK_PATH = "/webhook"


async def yookassa(request):
    body = await request.read()
    signature = request.headers.get("Signature", "")
    ok = await asyncio.to_thread(payments.process_notification, body, signature)
    return web.Response(status=200 if ok else 403, text="ok" if ok else "bad signature")


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
    app.router.add_post("/yookassa", yookassa)
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
    await site.start()

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
