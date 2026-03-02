import os
import logging
from flask import Flask
from .config import Config
from .db import init_db

# configure logging once
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_app():
    """Application factory for the Lost-and-Found app."""
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    # ensure upload directory exists early (configuration only)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    logger.info(f"Upload folder configured: {app.config['UPLOAD_FOLDER']}")

    # register blueprint containing all routes
    from . import routes  # imported here to avoid circular imports
    app.register_blueprint(routes.bp)

    # initialize database schema
    with app.app_context():
        init_db()

    return app


# expose a module-level app for gunicorn run:app
app = create_app()
