# Quick Start Guide

## Development Setup

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create .env File for Development
```bash
echo "FLASK_ENV=development" > .env
echo "SECRET_KEY=dev-secret-key" >> .env
echo "ADMIN_PASSWORD=admin123" >> .env
```

### 4. Run Development Server
```bash
python app.py
```

Server will start at `http://localhost:5000`

### 5. Access the App
- **Home** (Public): http://localhost:5000/
- **Report Item**: http://localhost:5000/report
- **Admin Dashboard**: http://localhost:5000/admin/login (Password: `admin123`)

---

## Production Deployment

For production deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)

**Quick command:**
```bash
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

---

## Key Features

✅ Report lost/found items with optional images
✅ Admin approval system
✅ Auto-delete images 24 hours after marking as returned  
✅ Responsive 2-column mobile layout
✅ Contact information sharing
✅ Item status tracking (pending/approved/returned)

---

## File Structure

```
lost-and-found/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── DEPLOYMENT.md         # Production deployment guide
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
│
├── static/
│   ├── styles.css        # CSS styling
│   ├── main.js           # JavaScript utilities
│   └── uploads/          # Uploaded images (auto-generated)
│
└── templates/
    ├── base.html         # Base template
    ├── index.html        # Home page
    ├── report.html       # Report item form
    ├── admin_login.html  # Admin login
    └── admin.html        # Admin dashboard
```

---

## Environment Variables

| Variable | Purpose | Development Default |
|----------|---------|----------------------|
| `FLASK_ENV` | Set mode | `development` |
| `SECRET_KEY` | Session encryption | `dev-secret-key` |
| `ADMIN_PASSWORD` | Admin login | `admin123` |
| `PORT` | Server port | `5000` |

Set `FLASK_ENV=production` before deploying to a server.

---

## Troubleshooting

**Images not showing?**
- Ensure images are in `static/uploads/`
- Check file permissions

**Admin login not working?**
- Navigate to http://localhost:5000/admin/login
- Default password: `` (change in production!)

**Port 5000 already in use?**
- Change in `.env`: `PORT=8000`
- Or kill process: `lsof -ti:5000 | xargs kill -9`

---

For more details, see [DEPLOYMENT.md](DEPLOYMENT.md)
