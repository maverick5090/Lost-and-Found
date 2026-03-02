from .db import get_db_connection
from datetime import datetime


# simple data-access functions to keep SQL out of routes

def fetch_public_items():
    conn = get_db_connection()
    items = conn.execute(
        "SELECT * FROM items WHERE approved = 1 AND status != 'returned' ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return items


def fetch_all_items():
    conn = get_db_connection()
    items = conn.execute("SELECT * FROM items ORDER BY id DESC").fetchall()
    conn.close()
    return items


def insert_item(item_type, name, description, location, contact, image_path=None):
    conn = get_db_connection()
    conn.execute(
        """
        INSERT INTO items (type, name, description, location, contact, status, approved, image)
        VALUES (?, ?, ?, ?, ?, 'pending', 0, ?)
        """,
        (item_type, name, description, location, contact, image_path),
    )
    conn.commit()
    conn.close()


def update_approve(item_id):
    conn = get_db_connection()
    conn.execute("UPDATE items SET approved = 1 WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()


def update_return(item_id):
    conn = get_db_connection()
    conn.execute(
        "UPDATE items SET status = 'returned', date_returned = ? WHERE id = ?",
        (datetime.now().isoformat(), item_id),
    )
    conn.commit()
    conn.close()
