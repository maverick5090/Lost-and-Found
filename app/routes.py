import os
import uuid
import logging
from functools import wraps
from datetime import datetime
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session,
    current_app,
)
from werkzeug.utils import secure_filename

from . import models
from .db import get_db_connection

bp = Blueprint("main", __name__)
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def is_admin_logged_in():
    return session.get("is_admin") is True


def admin_login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not is_admin_logged_in():
            next_url = request.path
            return redirect(url_for("main.admin_login", next=next_url))
        return view_func(*args, **kwargs)

    return wrapped


def cleanup_old_images():
    """Delete images that are 24+ hours old and marked as returned"""
    try:
        conn_items = models.fetch_all_items()
        now = datetime.now()
        deleted_count = 0
        for item in conn_items:
            if item["status"] == "returned" and item["date_returned"]:
                try:
                    returned_time = datetime.fromisoformat(item["date_returned"])
                    time_diff = (now - returned_time).total_seconds()
                    if time_diff >= 86400 and item.get("image"):
                        image_path = os.path.join(current_app.root_path, "static", item["image"])
                        if os.path.exists(image_path):
                            os.remove(image_path)
                            deleted_count += 1
                        # clear image reference in db
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


@bp.route("/")
def home():
    items = models.fetch_public_items()
    return render_template("index.html", items=items)


@bp.route("/report")
def report():
    return render_template("report.html")


@bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None
    next_url = request.args.get("next") or url_for("main.admin_dashboard")

    if request.method == "POST":
        password = request.form.get("password", "")
        if password == current_app.config["ADMIN_PASSWORD"]:
            session["is_admin"] = True
            return redirect(next_url)
        error = "Incorrect password."

    return render_template("admin_login.html", error=error)


@bp.route("/admin/logout", methods=["POST"])
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("main.home"))


@bp.route("/admin")
@admin_login_required
def admin_dashboard():
    items = models.fetch_all_items()
    return render_template("admin.html", items=items)


@bp.route("/item", methods=["POST"])
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
                unique_name = (
                    f"{uuid.uuid4().hex}_{safe_name}"
                    if safe_name
                    else f"{uuid.uuid4().hex}.{ext}"
                )
                try:
                    upload_folder = current_app.config["UPLOAD_FOLDER"]
                    f.save(os.path.join(upload_folder, unique_name))
                    image_path = f"uploads/{unique_name}"
                    logger.info(f"Image uploaded: {unique_name}")
                except Exception as e:
                    logger.error(f"Failed to save image: {str(e)}")
                    return "Failed to save image", 500

        models.insert_item(item_type, name, description, location, contact, image_path)
        logger.info(f"New item created: {item_type} - {name}")

        return redirect(url_for("main.home"))
    except Exception as e:
        logger.error(f"Error creating item: {str(e)}")
        return "An error occurred", 500


@bp.route("/items")
def list_items_api():
    items = models.fetch_public_items()
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


@bp.route("/admin/items")
@admin_login_required
def admin_items_api():
    items = models.fetch_all_items()
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


@bp.route("/admin/approve/<int:item_id>", methods=["POST"])
@admin_login_required
def approve_item(item_id):
    models.update_approve(item_id)
    return redirect(url_for("main.admin_dashboard"))


@bp.route("/admin/return/<int:item_id>", methods=["POST"])
@admin_login_required
def return_item(item_id):
    models.update_return(item_id)
    return redirect(url_for("main.admin_dashboard"))
