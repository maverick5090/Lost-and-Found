import os
import logging
from flask import Flask
from .config import Config
from .db import init_db
from apscheduler.schedulers.background import BackgroundScheduler

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

    # initialize database and scheduler
    with app.app_context():
        init_db()
        _init_scheduler(app)

    return app


# expose app at package level for WSGI servers (e.g. gunicorn app:app)
# this is optional but provides a fallback if run.py is not used.
app = create_app()


def _init_scheduler(app):
    """Internal helper to start the background cleanup job."""
    # import routes here to avoid circular import at module load time
    from . import routes

    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            func=routes.cleanup_old_images,
            trigger="interval",
            hours=1,
            id="cleanup_images",
        )
        scheduler.start()
        logger.info("Background scheduler started successfully")
        return scheduler
    except Exception as e:
        logger.error(f"Failed to start scheduler: {str(e)}")
        return None
