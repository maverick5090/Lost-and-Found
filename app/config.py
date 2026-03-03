import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# base directory is project root
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD") or "admin123"

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "uploads")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB

    DEBUG = os.environ.get("FLASK_ENV") == "development"

    DB_SSLMODE = os.environ.get("DB_SSLMODE", "require")
    DB_CONNECT_TIMEOUT = int(os.environ.get("DB_CONNECT_TIMEOUT", 10))
    DB_STATEMENT_TIMEOUT_MS = int(os.environ.get("DB_STATEMENT_TIMEOUT_MS", 10000))
