# Campus Lost & Found - Deployment Guide

## Production Deployment Instructions

### Prerequisites
- Python 3.8+
- pip or conda
- Linux/Unix server (or Windows with proper configuration)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables
Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` with your production values:
```
FLASK_ENV=production
PORT=5000
SECRET_KEY=generate-a-strong-random-key-here
ADMIN_PASSWORD=your-strong-admin-password
```

**To generate a strong SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 3: Initialize Database
```bash
python app.py
```
This will create the SQLite database and tables. Stop the app after initialization.

### Step 4: Deploy with Gunicorn

**Single process (small deployments):**
```bash
gunicorn --workers 1 --bind 0.0.0.0:5000 app:app
```

**Multiple processes (recommended for production):**
```bash
gunicorn --workers 4 --worker-class sync --bind 0.0.0.0:5000 app:app
```

**With logging:**
```bash
gunicorn --workers 4 \
  --bind 0.0.0.0:5000 \
  --access-logfile - \
  --error-logfile - \
  --log-level info \
  app:app
```

### Step 5: Use a Process Manager (Recommended)

**Using systemd (Linux):**

Create `/etc/systemd/system/lost-found.service`:
```ini
[Unit]
Description=Campus Lost & Found
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/lost-and-found
Environment="PATH=/path/to/venv/bin"
EnvironmentFile=/path/to/lost-and-found/.env
ExecStart=/path/to/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable lost-found
sudo systemctl start lost-found
```

### Step 6: Reverse Proxy Configuration (Nginx)

Create `/etc/nginx/sites-available/lost-found`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/lost-and-found/static/;
        expires 30d;
    }
}
```

Enable and test:
```bash
sudo ln -s /etc/nginx/sites-available/lost-found /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 7: SSL/TLS with Let's Encrypt

Install Certbot:
```bash
sudo apt-get install certbot python3-certbot-nginx
```

Get certificate:
```bash
sudo certbot --nginx -d your-domain.com
```

### Security Best Practices

✅ **DONE:**
- Environment variables for secrets (not hardcoded)
- Input validation and length checks
- Secure file upload handling
- SQL injection protection (parameterized queries)
- File size limits (10MB)
- Logging for monitoring

✅ **RECOMMENDED ADDITIONS:**
- Use PostgreSQL instead of SQLite for production
- Store images on cloud storage (AWS S3, Google Cloud)
- Enable CORS only for trusted domains
- Add rate limiting on endpoints
- Implement HTTPS/SSL (use Let's Encrypt)
- Set up security headers (CSP, X-Frame-Options, etc.)
- Regular database backups
- Monitor logs with ELK stack or similar

### Database Upgrade Path

To migrate from SQLite to PostgreSQL:

1. Install PostgreSQL dependencies:
```bash
pip install psycopg2-binary
```

2. Update connection in app.py (future enhancement)
3. Use a migration tool like Alembic
4. Backup SQLite data before migration

### Monitoring

Check application logs:
```bash
# If using systemd
sudo journalctl -u lost-found -f

# If running standalone
tail -f /var/log/lost-found/app.log
```

### Troubleshooting

- **Port already in use:** Change PORT in .env or kill process on port 5000
- **Permission denied for uploads:** Ensure socket user has write access to `static/uploads/`
- **Images not uploading:** Check `MAX_CONTENT_LENGTH` (currently 10MB)
- **Scheduler not running:** Check logs for APScheduler errors

### Environment Variables Reference

| Variable | Required | Default | Notes |
|----------|----------|---------|-------|
| FLASK_ENV | No | development | Set to 'production' for deployment |
| SECRET_KEY | Yes* | dev-secret-key | Generate with: `python -c "import secrets; print(secrets.token_hex(32))"` |
| ADMIN_PASSWORD | Yes* | admin123 | Use strong password for production |
| PORT | No | 5000 | Change if port is in use |

*Should be set for production security

### Cleanup Task

The application automatically:
- Deletes images 24+ hours after items are marked as returned
- Runs every hour via APScheduler
- Logs cleanup activity to stdout/stderr

---

**Last Updated:** February 27, 2026
