import sqlite3

import config


def _conn():
    config.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT NOT NULL,
                package_id TEXT NOT NULL,
                stars INTEGER NOT NULL,
                rub REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT DEFAULT (datetime('now'))
            )
            """
        )


def create_order(user_id, username, package_id, stars, rub):
    with _conn() as conn:
        cur = conn.execute(
            "INSERT INTO orders (user_id, username, package_id, stars, rub) VALUES (?,?,?,?,?)",
            (user_id, username, package_id, stars, rub),
        )
        return cur.lastrowid


def get_order(order_id):
    with _conn() as conn:
        row = conn.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
    return dict(row) if row else None


def set_status(order_id, status):
    with _conn() as conn:
        conn.execute("UPDATE orders SET status=? WHERE id=?", (status, order_id))


def list_user_orders(user_id):
    with _conn() as conn:
        rows = conn.execute(
            "SELECT * FROM orders WHERE user_id=? ORDER BY id DESC LIMIT 20",
            (user_id,),
        ).fetchall()
    return [dict(r) for r in rows]
