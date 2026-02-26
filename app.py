import sqlite3
import os
import uuid
import logging
from functools import wraps
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from werkzeug.utils import secure_filename
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Security Configuration
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
if not ADMIN_PASSWORD:
    logger.warning("ADMIN_PASSWORD not set in environment variables. Please set a strong password.")
    ADMIN_PASSWORD = "admin123"  # Fallback for development only

app.secret_key = os.environ.get("SECRET_KEY")
if not app.secret_key:
    logger.warning("SECRET_KEY not set in environment variables. Using development default. This is insecure for production.")
    app.secret_key = "dev-secret-key"

app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
app.config['DEBUG'] = os.environ.get('FLASK_ENV') == 'development'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
logger.info(f"Upload folder configured: {UPLOAD_FOLDER}")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def init_db():
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


def is_admin_logged_in():
    return session.get("is_admin") is True


def cleanup_old_images():
    """Delete images that are 24+ hours old and marked as returned"""
    try:
        conn = get_db_connection()
        items = conn.execute(
            "SELECT id, image, date_returned FROM items WHERE status = 'returned' AND date_returned IS NOT NULL"
        ).fetchall()
        conn.close()
        
        now = datetime.now()
        deleted_count = 0
        for item in items:
            if item["date_returned"]:
                try:
                    returned_time = datetime.fromisoformat(item["date_returned"])
                    time_diff = (now - returned_time).total_seconds()
                    # 86400 seconds = 24 hours
                    if time_diff >= 86400 and item["image"]:
                        image_path = os.path.join(BASE_DIR, "static", item["image"])
                        if os.path.exists(image_path):
                            os.remove(image_path)
                            deleted_count += 1
                        # Set image to None in database
                        conn = get_db_connection()
                        conn.execute("UPDATE items SET image = NULL WHERE id = ?", (item["id"],))
                        conn.commit()
                        conn.close()
                except (ValueError, OSError) as e:
                    logger.error(f"Error processing item {item['id']}: {str(e)}")
        if deleted_count > 0:
            logger.info(f"Cleanup: Deleted {deleted_count} old images")
    except Exception as e:
        logger.error(f"Cleanup task failed: {str(e)}")


def admin_login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not is_admin_logged_in():
            next_url = request.path
            return redirect(url_for("admin_login", next=next_url))
        return view_func(*args, **kwargs)

    return wrapped


@app.route("/")
def home():
    conn = get_db_connection()
    # Only show approved items to public users
    items = conn.execute(
        "SELECT * FROM items WHERE approved = 1 AND status != 'returned' ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return render_template("index.html", items=items)


@app.route("/report")
def report():
    return render_template("report.html")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None
    next_url = request.args.get("next") or url_for("admin_dashboard")

    if request.method == "POST":
        password = request.form.get("password", "")
        if password == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(next_url)
        error = "Incorrect password."

    return render_template("admin_login.html", error=error)


@app.route("/admin/logout", methods=["POST"])
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("home"))


@app.route("/admin")
@admin_login_required
def admin_dashboard():
    conn = get_db_connection()
    items = conn.execute("SELECT * FROM items ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("admin.html", items=items)


@app.route("/item", methods=["POST"])
def create_item():
    try:
        item_type = request.form.get("type", "").strip()
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        location = request.form.get("location", "").strip()
        contact = request.form.get("contact", "").strip()

        if item_type not in ("lost", "found"):
            logger.warning(f"Invalid item type attempted: {item_type}")
            return "Invalid type", 400

        if not (name and description and location and contact):
            return "All fields are required.", 400

        # Validate input lengths
        if len(name) > 100 or len(description) > 500 or len(location) > 100:
            return "Input fields too long", 400

        image_path = None
        if "image" in request.files:
            f = request.files["image"]
            if f and f.filename and allowed_file(f.filename):
                ext = f.filename.rsplit(".", 1)[1].lower()
                safe_name = secure_filename(f.filename)
                unique_name = f"{uuid.uuid4().hex}_{safe_name}" if safe_name else f"{uuid.uuid4().hex}.{ext}"
                try:
                    f.save(os.path.join(UPLOAD_FOLDER, unique_name))
                    image_path = f"uploads/{unique_name}"
                    logger.info(f"Image uploaded: {unique_name}")
                except Exception as e:
                    logger.error(f"Failed to save image: {str(e)}")
                    return "Failed to save image", 500

        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO items (type, name, description, location, contact, status, approved, image)
            VALUES (?, ?, ?, ?, ?, 'pending', 0, ?)
            """,
            (item_type, name, description, location, contact, image_path),
        )
        conn.commit()
        conn.close()
        logger.info(f"New item created: {item_type} - {name}")

        return redirect(url_for("home"))
    except Exception as e:
        logger.error(f"Error creating item: {str(e)}")
        return "An error occurred", 500


@app.route("/items")
def list_items_api():
    conn = get_db_connection()
    # API returns only approved items (public)
    items = conn.execute("SELECT * FROM items WHERE approved = 1 AND status != 'returned' ORDER BY id DESC").fetchall()
    conn.close()
    data = [
        {
            "id": row["id"],
            "type": row["type"],
            "name": row["name"],
            "description": row["description"],
            "location": row["location"],
            "contact": row["contact"],
            "status": row["status"],
            "approved": bool(row["approved"]),
            "image": row["image"] if "image" in row.keys() and row["image"] else None,
        }
        for row in items
    ]
    return jsonify(data)


@app.route("/admin/items")
@admin_login_required
def admin_items_api():
    conn = get_db_connection()
    items = conn.execute("SELECT * FROM items ORDER BY id DESC").fetchall()
    conn.close()
    data = [
        {
            "id": row["id"],
            "type": row["type"],
            "name": row["name"],
            "description": row["description"],
            "location": row["location"],
            "contact": row["contact"],
            "status": row["status"],
            "approved": bool(row["approved"]),
            "image": row["image"] if "image" in row.keys() and row["image"] else None,
        }
        for row in items
    ]
    return jsonify(data)


@app.route("/admin/approve/<int:item_id>", methods=["POST"])
@admin_login_required
def approve_item(item_id):
    conn = get_db_connection()
    conn.execute(
        "UPDATE items SET approved = 1 WHERE id = ?",
        (item_id,),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/return/<int:item_id>", methods=["POST"])
@admin_login_required
def return_item(item_id):
    conn = get_db_connection()
    conn.execute(
        "UPDATE items SET status = 'returned', date_returned = ? WHERE id = ?",
        (datetime.now().isoformat(), item_id),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("admin_dashboard"))


def init_scheduler():
    """Initialize background scheduler for cleanup tasks"""
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=cleanup_old_images, trigger="interval", hours=1, id='cleanup_images')
        scheduler.start()
        logger.info("Background scheduler started successfully")
        return scheduler
    except Exception as e:
        logger.error(f"Failed to start scheduler: {str(e)}")
        return None


if __name__ == "__main__":
    with app.app_context():
        init_db()
    
    # Setup background scheduler for cleaning up old images
    scheduler = init_scheduler()
    
    # Determine debug mode from environment
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    port = int(os.environ.get('PORT', 5000))
    
    if debug_mode:
        logger.warning("Running in development mode. Set FLASK_ENV to production for deployment.")
    else:
        logger.info("Running in production mode. Use Gunicorn or similar WSGI server for deployment.")
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)

