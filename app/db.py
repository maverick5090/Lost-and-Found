import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app


def _required_db_config():
    return {
        "DB_HOST": current_app.config.get("DB_HOST"),
        "DB_USER": current_app.config.get("DB_USER"),
        "DB_PASSWORD": current_app.config.get("DB_PASSWORD"),
        "DB_NAME": current_app.config.get("DB_NAME"),
        "DB_PORT": current_app.config.get("DB_PORT"),
    }


def get_db_connection():
    """
    Return a PostgreSQL connection using Supabase credentials.
    The connection uses autocommit so callers do not need to manage transactions.
    Uses RealDictCursor so rows behave like dicts (row['column']).
    """
    config = _required_db_config()
    missing = [key for key, value in config.items() if value in (None, "")]
    if missing:
        missing_list = ", ".join(missing)
        raise RuntimeError(f"Missing required database config: {missing_list}")

    conn = psycopg2.connect(
        host=current_app.config["DB_HOST"],
        user=current_app.config["DB_USER"],
        password=current_app.config["DB_PASSWORD"],
        dbname=current_app.config["DB_NAME"],
        port=current_app.config["DB_PORT"],
        sslmode=current_app.config["DB_SSLMODE"],
        connect_timeout=current_app.config["DB_CONNECT_TIMEOUT"],
        cursor_factory=RealDictCursor,
        options=f"-c statement_timeout={current_app.config['DB_STATEMENT_TIMEOUT_MS']}",
    )
    conn.autocommit = True
    return conn


def init_db():
    """
    Initialize the database schema if it does not already exist.
    Creates the `items` table using PostgreSQL-compatible SQL.
    """
    conn = get_db_connection()
    cur = None
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id SERIAL PRIMARY KEY,
                type TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                location TEXT NOT NULL,
                contact TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                approved BOOLEAN DEFAULT FALSE,
                image TEXT,
                date_returned TIMESTAMP
            );
            """
        )
    finally:
        if cur is not None:
            cur.close()
        conn.close()
