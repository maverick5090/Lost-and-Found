from .db import get_db_connection
from contextlib import closing
from datetime import datetime


# simple data-access functions to keep SQL out of routes

def fetch_public_items():
    with closing(get_db_connection()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM items WHERE approved = 1 AND status != 'returned' ORDER BY id DESC"
            )
            return cur.fetchall()


def fetch_all_items():
    with closing(get_db_connection()) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM items ORDER BY id DESC")
            return cur.fetchall()


def insert_item(item_type, name, description, location, contact, image_path=None):
    with closing(get_db_connection()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO items (type, name, description, location, contact, status, approved, image)
                VALUES (%s, %s, %s, %s, %s, 'pending', 0, %s)
                """,
                (item_type, name, description, location, contact, image_path),
            )


def update_approve(item_id):
    with closing(get_db_connection()) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE items SET approved = 1 WHERE id = %s", (item_id,))


def update_return(item_id):
    with closing(get_db_connection()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE items SET status = 'returned', date_returned = %s WHERE id = %s",
                (datetime.now().isoformat(), item_id),
            )


def clear_item_images(item_ids):
    if not item_ids:
        return

    with closing(get_db_connection()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE items SET image = NULL WHERE id = ANY(%s)",
                (item_ids,),
            )
