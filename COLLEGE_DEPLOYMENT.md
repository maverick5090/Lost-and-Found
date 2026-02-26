# Campus Lost & Found - Production Deployment for College

## Recommended Setup for 500+ Students

**Best Option:** Heroku or PythonAnywhere (easiest for colleges)
**For scalability:** AWS or Google Cloud Platform

---

## Option 1: Heroku (Recommended - Easiest)

### Pros:
✅ Free tier available  
✅ Auto-scaling  
✅ Simple deployment (git push)  
✅ Built-in PostgreSQL option  
✅ Email notifications included  

### Step 1: Create Heroku Account
1. Go to [heroku.com](https://www.heroku.com)
2. Sign up (free account)
3. Verify email

### Step 2: Install Heroku CLI
```bash
# Windows
choco install heroku-cli
# or download from: https://devcenter.heroku.com/articles/heroku-cli

# Then verify
heroku --version
```

### Step 3: Login to Heroku
```bash
cd "d:\Codes\Hackathons\lost and found"
heroku login
```
Opens browser to authenticate

### Step 4: Create Heroku App
```bash
heroku create lost-found-college
# Replace with your app name
```

### Step 5: Add PostgreSQL Database
```bash
heroku addons:create heroku-postgresql:hobby-dev -a lost-found-college
```
This adds free PostgreSQL database

### Step 6: Update app.py for PostgreSQL

Add to `app.py` after imports:

```python
import psycopg2
from psycopg2.extras import RealDictCursor

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    if DATABASE_URL:
        # PostgreSQL for production
        conn = psycopg2.connect(DATABASE_URL)
        conn.row_factory = RealDictCursor
    else:
        # SQLite for development
        import sqlite3
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
    return conn
```

Actually, I'll provide a simpler approach below...

### Step 7: Update requirements.txt

```
Flask>=2.3.0
APScheduler>=3.10.0
Gunicorn>=21.0.0
python-dotenv>=1.0.0
psycopg2-binary>=2.9.0
```

### Step 8: Create Procfile

Create file: `Procfile` (no extension)
```
web: gunicorn app:app
```

### Step 9: Deploy to Heroku

```bash
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main
```

### Step 10: Initialize Database

```bash
heroku run python -a lost-found-college
# In Python shell:
# from app import init_db, app
# with app.app_context():
#     init_db()
# exit()
```

### Step 11: Get Live URL

```bash
heroku open -a lost-found-college
```

Your app is live! Share URL with students.

---

## Option 2: PythonAnywhere (Very Easy)

### Step 1: Sign Up
- Go to [pythonanywhere.com](https://www.pythonanywhere.com)
- Free account (500MB storage, one web app)

### Step 2: Clone Repository
- Go to **Web** tab
- Add new web app
- Choose Python 3.x
- Choose Flask

### Step 3: Upload Code
- Upload files via web interface
- Or use git:
```bash
git clone https://github.com/maverick5090/Lost-and-Found.git
```

### Step 4: Run App
Start web app and visit your URL

---

## Option 3: AWS (Most Scalable)

### Services Needed:
- **EC2** - Virtual server
- **RDS** - PostgreSQL database
- **S3** - Image storage
- **Route 53** - Domain management

### Estimated Cost: $10-50/month for 500+ users

Follow [DEPLOYMENT.md](DEPLOYMENT.md) for detailed AWS setup.

---

## Configuration for College Use

### Set Strong Admin Password

Create `.env`:
```env
FLASK_ENV=production
PORT=5000
SECRET_KEY=generate-with: python -c "import secrets; print(secrets.token_hex(32))"
ADMIN_PASSWORD=your-strong-college-password
DATABASE_URL=postgresql://... (Heroku provides this)
USE_S3=true  # Optional: for image storage
```

### Enable Email Notifications (Optional)

Add to `requirements.txt`:
```
Flask-Mail>=0.9.1
```

Add to app.py:
```python
from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', True)
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)

# In create_item(), after saving:
msg = Message(
    subject=f'New {item_type} item reported',
    recipients=['admin@college.edu']
)
mail.send(msg)
```

---

## College-Specific Features to Add

### 1. Student Authentication (Optional)

Modify `admin_login_required` to check college email:

```python
def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        # Optional: Check for college email domain
        if not session.get("is_admin"):
            return redirect(url_for("admin_login"))
        return view_func(*args, **kwargs)
    return wrapped
```

### 2. Campus Locations

Update `report.html` form:
```html
<select name="location" required>
    <option value="">Select Location</option>
    <option value="Library">Library</option>
    <option value="Cafeteria">Cafeteria</option>
    <option value="Hostel A">Hostel A</option>
    <option value="Sports Complex">Sports Complex</option>
    <option value="Chemistry Building">Chemistry Building</option>
    <!-- Add more campus locations -->
</select>
```

### 3. Student Club Integration

Add to `templates/base.html`:
```html
<p style="text-align: center; color: var(--text-muted); margin-top: 20px;">
    Managed by: Campus Safety Committee | 📧 lostfound@college.edu
</p>
```

---

## Deployment Checklist

### Before Going Live:

- [ ] Update admin password in `.env`
- [ ] Set strong `SECRET_KEY`
- [ ] Configure database (PostgreSQL recommended)
- [ ] Test with 50+ simultaneous users
- [ ] Enable HTTPS (automatic on Heroku)
- [ ] Set up SSL certificate
- [ ] Create college domain (lost-and-found.college.edu)
- [ ] Test file uploads
- [ ] Test image cleanup (24-hour task)
- [ ] Plan backup strategy
- [ ] Set up monitoring/alerts

### Ongoing Maintenance:

- [ ] Daily: Check admin dashboard for new items
- [ ] Weekly: Review and approve items
- [ ] Weekly: Check application logs for errors
- [ ] Monthly: Backup database
- [ ] Monthly: Review usage statistics

---

## Monitoring & Support

### Set Up Error Alerts

For Heroku:
```bash
heroku logs -a lost-found-college -t  # Real-time logs
heroku logs -a lost-found-college --num 100  # Last 100 lines
```

### Monitor Performance

```bash
heroku ps:scale web=2 -a lost-found-college  # Scale to 2 dynos for high traffic
```

---

## Costs Breakdown

| Service | Price | Notes |
|---------|-------|-------|
| **Heroku** | Free-$7/month | Hobby tier = free with limits |
| **PostgreSQL** | Free-$9/month | Heroku addon |
| **SSL** | Free | Included |
| **S3 (optional)** | $0.02/GB | Only if storing many images |
| **Total** | ~$7-20/month | Very affordable for college |

---

## Student Instructions

Share with students:

```
# Campus Lost & Found

Report lost or found items on campus!

## How to Use:

1. **Report Item**: Click "Report Item" button
2. **Fill Form**: Item type, description, location, contact
3. **Upload Photo**: Optional but recommended
4. **Submit**: Your item is submitted for review

## Rules:

- Be honest and accurate
- Include your contact info
- Be respectful to other users
- Photos auto-delete 24 hours after item marked as returned

## Admin Access:

Staff only: admin@lost-and-found.edu
```

---

## Going Live - Quick Checklist

```bash
# 1. Test everything locally
python app.py
# Visit http://localhost:5000

# 2. Push to GitHub
git add .
git commit -m "Ready for production"
git push origin main

# 3. Deploy to Heroku
git push heroku main

# 4. Verify production
heroku open

# 5. Share with students!
```

---

## Troubleshooting

**App not running on Heroku:**
```bash
heroku logs -t -a lost-found-college
```

**Database connection error:**
```bash
heroku config -a lost-found-college
# Check DATABASE_URL is set
```

**Images not saving:**
- Check S3 credentials (if using S3)
- Check file permissions
- Check disk space

---

## Next Steps

1. **Choose hosting**: Heroku (easiest) or AWS (scalable)
2. **Deploy**: Follow steps above
3. **Test**: Ask 10 students to beta test
4. **Promote**: Announce on campus notice boards, email
5. **Monitor**: Check logs and feedback daily

---

## Support

For deployment help:
- Heroku docs: https://devcenter.heroku.com
- Flask docs: https://flask.palletsprojects.com
- GitHub Issues: Post on your repo

Good luck with your hackathon project! 🎓
