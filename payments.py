import base64
import hashlib
import hmac
import json

import requests

import config
from db import set_status


def _ready():
    return bool(config.YUKASSA_SHOP_ID and config.YUKASSA_SECRET)


def create_payment(order_id, rub, description):
    if not _ready():
        return None
    payload = {
        "amount": {"value": f"{rub:.2f}", "currency": "RUB"},
        "capture": True,
        "confirmation": {"type": "redirect", "return_url": config.RETURN_URL},
        "description": description,
        "metadata": {"order_id": str(order_id)},
    }
    resp = requests.post(
        "https://api.yookassa.ru/v3/payments",
        json=payload,
        auth=(config.YUKASSA_SHOP_ID, config.YUKASSA_SECRET),
        timeout=15,
    )
    if resp.status_code == 200:
        return resp.json()["confirmation"]["confirmation_url"]
    return None


def verify_signature(body: bytes, signature: str) -> bool:
    if not _ready():
        return False
    digest = hmac.new(config.YUKASSA_SECRET.encode(), body, hashlib.sha256).digest()
    expected = base64.b64encode(digest).decode()
    return hmac.compare_digest(expected, signature or "")


def process_notification(body: bytes, signature: str) -> bool:
    if not verify_signature(body, signature):
        return False
    data = json.loads(body)
    if data.get("event") != "payment.succeeded":
        return True
    order_id = int(data["object"]["metadata"]["order_id"])
    set_status(order_id, "paid")
    import stars

    stars.deliver(order_id)
    return True
