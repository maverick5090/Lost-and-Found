import os
import logging
from flask import Flask
from .config import Config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    # PostgreSQL (Supabase) config from Render env vars
    app.config["DB_HOST"] = os.getenv("DB_HOST")
    app.config["DB_USER"] = os.getenv("DB_USER")
    app.config["DB_PASSWORD"] = os.getenv("DB_PASSWORD")
    app.config["DB_NAME"] = os.getenv("DB_NAME")
    app.config["DB_PORT"] = int(os.getenv("DB_PORT", 5432))

    # Upload folder
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    logger.info(f"Upload folder configured: {app.config['UPLOAD_FOLDER']}")

    # Register routes
    from .routes import main
    app.register_blueprint(main)

    return app