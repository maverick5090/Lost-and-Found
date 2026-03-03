🧳 Campus Lost & Found

A simple and practical Lost & Found web application built for college campuses.
Students can report lost or found items, and an admin can review and approve listings before they are publicly visible.

🔗 Live Demo:
https://lost-and-found-crgt.onrender.com/

⚠️ Note: The first load may take 30–60 seconds because the app is hosted on a free Render instance that sleeps during inactivity.

🎯 Problem Statement

In college campuses, lost items are usually reported via informal WhatsApp groups or word of mouth, which is inefficient and unorganized.
This project provides a centralized digital platform where students can report and discover lost or found items in a structured way.

✅ Features
Student Side

View approved lost & found items

Report a lost or found item using a simple form

No login required (kept simple for accessibility)

Admin Side

Admin-only approval workflow

Approve or reject reported items

Control what appears publicly

🛠️ Tech Stack

Frontend

HTML

CSS

JavaScript

Jinja2 Templates

Backend

Python

Flask (Application Factory Pattern)

Database

PostgreSQL (Supabase/Render compatible)

Automatic schema initialization (`init_db`)

Deployment

Render

Gunicorn (WSGI server)

🧱 Project Structure
Lost-and-Found/
├── app/
│   ├── __init__.py        # create_app() and app setup
│   ├── routes.py          # Flask routes (Blueprint)
│   ├── models.py          # DB query logic
│   ├── db.py              # PostgreSQL connection & init_db()
│   ├── templates/         # HTML templates
│   └── static/            # CSS, JS, uploads
│
├── run.py                 # Gunicorn entry point
├── requirements.txt
└── README.md
⚙️ How the App Works (High Level)

Flask app starts using an application factory (create_app)

Database schema is initialized automatically using:

CREATE TABLE IF NOT EXISTS

Users submit lost/found items

Items remain hidden until approved by admin

Approved items appear on the public homepage

This approach makes the app portable across environments without manual database setup.

🧪 Database Initialization (Important)

The database schema is created automatically on startup:

No manual SQL execution required

Safe to run multiple times

Prevents no such table errors on deployment

This is handled inside the app factory using app.app_context().

🚀 Running Locally
1️⃣ Clone the repository
git clone https://github.com/maverick5090/Lost-and-Found.git
cd Lost-and-Found
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Run the app
python run.py

The app will be available at:

http://127.0.0.1:5000
☁️ Deployment Notes (Render)

Hosted on Render Free Tier

App may take time to wake up after inactivity

Use managed PostgreSQL for persistent storage across deploys and restarts.

🔐 Admin Access

Admin approval logic is implemented on the backend

Authentication is intentionally kept simple for college demo use

Can be extended with proper login/auth in future versions

📌 Limitations

No user authentication (by design)

Database layer is PostgreSQL-backed for production workloads.

Free hosting causes cold-start delays

📈 Future Improvements

User authentication (student login)

Database migrations and backups for PostgreSQL

Image uploads with moderation

Search and category filters

Email or notification system

🎓 Academic Note

This project is built as a college-level full-stack web application to demonstrate:

Backend development with Flask

Proper deployment practices

Debugging real production issues

Clean project structure

👤 Author

Devesh Agre
B.Tech CSE Student

📜 License

This project is for educational purposes.


