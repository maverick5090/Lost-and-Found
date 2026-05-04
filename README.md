# 🧳 Campus Lost & Found

A centralized Lost & Found platform designed for college campuses.
Students can report lost or found items, while an admin reviews and approves submissions before they are publicly visible.

🔗 **Live Demo**
https://lost-and-found-crgt.onrender.com/

> ⚠️ Note: The app may take 30–60 seconds to load initially due to free-tier hosting on Render.

---

## 🎯 Problem

Lost items on campuses are typically handled through WhatsApp groups or word of mouth — which is unstructured, unreliable, and inefficient.

This project solves that by providing:

* A single, organized platform
* Structured item reporting
* Admin-controlled visibility

---

## ⚙️ Key Features

### 👨‍🎓 Student Side

* View all approved lost & found items
* Submit a lost or found report via a simple form
* No login required (fast and accessible)

### 🛠️ Admin Side

* Review submitted items
* Approve or reject listings
* Control what appears publicly

---

## 🧠 How It Works

* Users submit items through a form
* Items are stored in the database but remain hidden
* Admin reviews submissions
* Approved items are displayed on the public homepage

---

## 🏗️ Tech Stack

### Frontend

* HTML
* CSS
* JavaScript
* Jinja2 (templating)

### Backend

* Python
* Flask (Application Factory Pattern)

### Database

* PostgreSQL (Render / Supabase compatible)

### Deployment

* Render (Free Tier)
* Gunicorn (WSGI server)

---

## 🧱 Project Structure

```
Lost-and-Found/
│
├── app/
│   ├── __init__.py      # App factory (create_app)
│   ├── routes.py        # Application routes
│   ├── models.py        # Database logic
│   ├── db.py            # PostgreSQL connection + init
│   ├── templates/       # HTML templates
│   └── static/          # CSS, JS, uploads
│
├── run.py               # Entry point (Gunicorn)
├── requirements.txt
└── README.md
```

---

## 🧪 Database Initialization

The database schema is automatically created on startup using:

* `CREATE TABLE IF NOT EXISTS`

### Why this matters:

* No manual SQL setup required
* Safe across deployments
* Prevents missing table errors

---

## 🚀 Run Locally

### 1. Clone the repo

```
git clone https://github.com/maverick5090/Lost-and-Found.git
cd Lost-and-Found
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Run the app

```
python run.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

## ☁️ Deployment

* Hosted on Render (free tier)
* Uses PostgreSQL for persistent storage
* Cold start delay due to inactivity

---

## 🔐 Admin Access

* Admin approval logic is implemented on backend
* Authentication is minimal (can be extended)

---

## 📉 Limitations

* No user authentication
* No image uploads
* Cold-start delays (free hosting)

---

## 📈 Future Improvements

* User authentication system (student login)
* Image upload + moderation
* Search and filters (category, keywords)
* Email/notification system
* Database migrations

---

## 🎓 Learning Outcomes

This project demonstrates:

* Full-stack web development using Flask
* Real-world deployment (Render + PostgreSQL)
* Application structuring using factory pattern
* Debugging production issues

---

## 👤 Author

**Devesh Agre**
B.Tech Computer Science Engineering

---

## 📜 License

This project is built for educational purposes.
