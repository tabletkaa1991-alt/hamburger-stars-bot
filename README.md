# Hamburger_Stars — бот по продаже Telegram-звёзд

## Установка
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Настройка
1. Скопируй `.env.example` в `.env` и заполни ключи (`.env` не коммитится).
2. `BOT_TOKEN` уже прописан.

## Запуск
```bash
python main.py           # сам бот (polling)
python webhook.py        # приём уведомлений ЮKassa (порт 8000)
```

## Структура
- `main.py` — запуск бота.
- `bot.py` — меню, каталог, заказы.
- `db.py` — SQLite (заказы).
- `payments.py` — ЮKassa: создание платежа + проверка подписи webhook.
- `stars.py` — выдача звёзд через Fragment.
- `webhook.py` — HTTP-сервер для уведомлений ЮKassa.

## Статусы заказа
`pending` → `paid` → `delivered` / `failed` / `manual`

## Безопасность
- Секреты только в `.env`, в git не попадают.
- Webhook проверяет подпись ЮKassa (HMAC-SHA256).
- `stars.py` использует отдельный Fragment-аккаунт с 2FA.
- Перед установкой `pyfragment` — проверить его исходник на утечку сессии.

## Что нужно доделать
1. Зарегистрировать ЮKassa → вписать `YUKASSA_SHOP_ID` и `YUKASSA_SECRET`.
2. Настроить webhook ЮKassa на HTTPS-адрес `/yookassa` (домен + SSL).
3. Заполнить `FRAGMENT_SESSION` (отдельный аккаунт Fragment).
4. Сверить сигнатуру `pyfragment` с его README перед включением автовыдачи.
