from .db import get_db_connection
from datetime import datetime


# simple data-access functions to keep SQL out of routes

def fetch_public_items():
    conn = get_db_connection()
    cur = None
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM items WHERE approved = TRUE AND status != 'returned' ORDER BY id DESC"
        )
        rows = cur.fetchall()
        return rows
    finally:
        if cur is not None:
            cur.close()
        conn.close()


def fetch_all_items():
    conn = get_db_connection()
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM items ORDER BY id DESC")
        rows = cur.fetchall()
        return rows
    finally:
        if cur is not None:
            cur.close()
        conn.close()


def insert_item(item_type, name, description, location, contact, image_path=None):
    conn = get_db_connection()
    cur = None
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO items (type, name, description, location, contact, status, approved, image)
            VALUES (%s, %s, %s, %s, %s, 'pending', FALSE, %s)
            """,
            (item_type, name, description, location, contact, image_path),
        )
    finally:
        if cur is not None:
            cur.close()
        conn.close()


def update_approve(item_id):
    item_id = int(item_id)
    conn = get_db_connection()
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("UPDATE items SET approved = TRUE WHERE id = %s", (item_id,))
    finally:
        if cur is not None:
            cur.close()
        conn.close()


def update_return(item_id):
    item_id = int(item_id)
    conn = get_db_connection()
    cur = None
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE items SET status = 'returned', date_returned = %s WHERE id = %s",
            (datetime.now(), item_id),
        )
    finally:
        if cur is not None:
            cur.close()
        conn.close()


def clear_item_images(item_ids):
    if not item_ids:
        return

    normalized_item_ids = [int(item_id) for item_id in item_ids]
    conn = get_db_connection()
    cur = None
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE items SET image = NULL WHERE id = ANY(%s)",
            (normalized_item_ids,),
        )
    finally:
        if cur is not None:
            cur.close()
        conn.close()
