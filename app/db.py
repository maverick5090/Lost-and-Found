import psycopg2
from flask import current_app


def get_db_connection():
    """
    Return a PostgreSQL connection using Supabase credentials.
    """
    return psycopg2.connect(
        host=current_app.config["DB_HOST"],
        user=current_app.config["DB_USER"],
        password=current_app.config["DB_PASSWORD"],
        dbname=current_app.config["DB_NAME"],
        port=current_app.config["DB_PORT"],
    )