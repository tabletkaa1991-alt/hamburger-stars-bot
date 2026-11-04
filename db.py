import psycopg2
import psycopg2.extras

import config


def _conn():
    return psycopg2.connect(config.DATABASE_URL, connect_timeout=20)


def init_db():
    with _conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                username TEXT NOT NULL,
                package_id TEXT NOT NULL,
                stars INTEGER NOT NULL,
                rub REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TIMESTAMPTZ NOT NULL DEFAULT now()
            )
            """
        )


def create_order(user_id, username, package_id, stars, rub):
    with _conn() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO orders (user_id, username, package_id, stars, rub) VALUES (%s,%s,%s,%s,%s) RETURNING id",
            (user_id, username, package_id, stars, rub),
        )
        return cur.fetchone()[0]


def get_order(order_id):
    with _conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM orders WHERE id=%s", (order_id,))
        row = cur.fetchone()
    return dict(row) if row else None


def set_status(order_id, status):
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("UPDATE orders SET status=%s WHERE id=%s", (status, order_id))


def list_user_orders(user_id):
    with _conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM orders WHERE user_id=%s ORDER BY id DESC LIMIT 20", (user_id,))
        rows = cur.fetchall()
    return [dict(r) for r in rows]
