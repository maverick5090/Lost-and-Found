import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app


def get_db_connection():
    """
    Return a PostgreSQL connection using Supabase credentials.
    The connection uses autocommit so callers do not need to manage transactions.
    Uses RealDictCursor so rows behave like dicts (row['column']).
    """
    conn = psycopg2.connect(
        host=current_app.config["DB_HOST"],
        user=current_app.config["DB_USER"],
        password=current_app.config["DB_PASSWORD"],
        dbname=current_app.config["DB_NAME"],
        port=current_app.config["DB_PORT"],
        cursor_factory=RealDictCursor,
    )
    conn.autocommit = True
    return conn


def init_db():
    """
    Initialize the database schema if it does not already exist.
    Creates the `items` table using PostgreSQL-compatible SQL.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS items (
                    id SERIAL PRIMARY KEY,
                    type TEXT NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    location TEXT NOT NULL,
                    contact TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    approved INTEGER NOT NULL DEFAULT 0,
                    image TEXT,
                    date_returned TIMESTAMP
                );
                """
            )
    finally:
        conn.close()
