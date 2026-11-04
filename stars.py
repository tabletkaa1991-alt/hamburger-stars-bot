import config
from db import get_order, set_status


def deliver(order_id):
    order = get_order(order_id)
    if not order or order["status"] != "paid":
        return

    if not config.FRAGMENT_SESSION:
        # Сессия Fragment не настроена — оставляем на ручную выдачу.
        set_status(order_id, "manual")
        return

    try:
        from pyfragment import Fragment

        client = Fragment(config.FRAGMENT_SESSION)
        # Точная сигнатура зависит от версии pyfragment — сверь с её README после аудита.
        client.purchase_stars(order["username"], order["stars"], payment_method=config.FRAGMENT_PAYMENT)
        set_status(order_id, "delivered")
    except Exception:
        set_status(order_id, "failed")
