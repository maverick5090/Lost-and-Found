import os
import logging
from flask import Flask
from .config import Config
from .db import init_db

# load logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_app():
    """Application factory for the Lost-and-Found app."""
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    # make sure upload dir exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    logger.info(f"Upload folder configured: {app.config['UPLOAD_FOLDER']}")

    # register routes
    from . import routes  # noqa: E402 - blueprint registered below

    app.register_blueprint(routes.bp)

    # initialize database
    with app.app_context():
        init_db()

    return app


# expose app at package level for WSGI servers (e.g. gunicorn app:app)
# this is optional but provides a fallback if run.py is not used.
app = create_app()


# scheduler support removed to avoid startup NameError on import
# the background job is no longer started during app creation.