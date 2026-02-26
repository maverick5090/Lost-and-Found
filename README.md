# Campus Lost & Found (Simple Flask Demo)

This is a beginner-friendly, hackathon-ready Campus Lost &amp; Found web app.

It uses:

- Python Flask
- SQLite
- Plain HTML, CSS, and a tiny bit of JavaScript

## Features

- Home page with navigation
- Report Lost / Found item form
- Public list of approved found items
- Simple admin dashboard (no login)
- Basic JSON APIs for items

## Quick Start

1. Create and activate a virtual environment (recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python app.py
```

4. Open the app in your browser:

- Main site: `http://127.0.0.1:5000/`
- Admin dashboard: `http://127.0.0.1:5000/admin`

## API Endpoints

- `POST /item` – submit lost or found item
- `GET /items` – list all items (approved &amp; pending)
- `GET /admin/items` – list all items (same as `/items`, for admin tools)
- `POST /admin/approve/<id>` – approve an item
- `POST /admin/return/<id>` – mark an item as returned

The database file `database.db` is created automatically on first run.

app.run(host="0.0.0.0", debug=True)

