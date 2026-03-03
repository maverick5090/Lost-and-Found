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
python run.py
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
goricorn --workers 4 --bind 0.0.0.0:5000 run:app
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
Lost-and-Found/
├── app/
│   ├── __init__.py          # create_app() factory
│   ├── routes.py            # all Flask routes
│   ├── db.py                # PostgreSQL helper
│   ├── models.py            # data access functions
│   ├── config.py            # environment config
│   ├── templates/           # Jinja HTML files
│   └── static/              # CSS, JS, images (includes uploads)
├── run.py                   # WSGI entry point (exports `app`)
├── requirements.txt
├── README.md
└── .gitignore
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

