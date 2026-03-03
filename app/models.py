from .db import get_db_connection
from datetime import datetime


# simple data-access functions to keep SQL out of routes

def fetch_public_items():
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM items WHERE approved = 1 AND status != 'returned' ORDER BY id DESC"
        )
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        conn.close()


def fetch_all_items():
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM items ORDER BY id DESC")
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        conn.close()


def insert_item(item_type, name, description, location, contact, image_path=None):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO items (type, name, description, location, contact, status, approved, image)
            VALUES (%s, %s, %s, %s, %s, 'pending', 0, %s)
            """,
            (item_type, name, description, location, contact, image_path),
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()


def update_approve(item_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("UPDATE items SET approved = 1 WHERE id = %s", (item_id,))
        conn.commit()
    finally:
        cur.close()
        conn.close()


def update_return(item_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE items SET status = 'returned', date_returned = %s WHERE id = %s",
            (datetime.now().isoformat(), item_id),
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()
