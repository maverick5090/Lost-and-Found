import sqlite3
from flask import current_app


def get_db_connection():
    """Return a sqlite3 connection using the configured DB path."""
    conn = sqlite3.connect(current_app.config['DB_PATH'])
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Ensure required tables and columns exist."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            location TEXT NOT NULL,
            contact TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            approved INTEGER NOT NULL DEFAULT 0
        );
        """
    )
    # alter statements are safe to run repeatedly
    try:
        cur.execute("ALTER TABLE items ADD COLUMN image TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cur.execute("ALTER TABLE items ADD COLUMN date_returned DATETIME")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()
