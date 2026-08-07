# AbleGod College E-Library

A fully-featured Django-based Electronic Library System for **AbleGod College** — designed to manage books, past exam papers, learning materials, borrowing, user roles (Admin, Teacher, Librarian, Student), and more.

> **Designed & Developed by BG DevOps** — 📞 0784654328

---

## Features

- 📚 Resource management (books, past papers, notes, learning materials)
- 👥 Role-based access: Admin, Teacher, Librarian, Student
- 🔐 Secure authentication and session management
- 📥 File upload and download system
- 📊 Dashboard with stats and quick access
- 🗂 Category, Department, Author filtering
- 📋 Borrowing / lending management
- 🔔 Notification system

---

## Tech Stack

- **Backend**: Django 5.x (Python)
- **Database**: SQLite (dev) / MySQL (production)
- **Static files**: WhiteNoise
- **Production server**: Gunicorn
- **Frontend**: Bootstrap 5 + Vanilla CSS

---

## Local Development Setup

```bash
# 1. Clone the repository
git clone https://github.com/BGSoftwares/AbleGodCollegeELibrary.git
cd AbleGodCollegeELibrary

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env with your local settings

# 5. Run migrations
python manage.py migrate

# 6. Create a superuser (admin)
python manage.py createsuperuser

# 7. Collect static files
python manage.py collectstatic --noinput

# 8. Start development server
python manage.py runserver
```

Open http://127.0.0.1:8000 in your browser.

---

## Production Deployment

### Environment Variables (set on your hosting platform)

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Long random Django secret key |
| `DEBUG` | Set to `False` in production |
| `ALLOWED_HOSTS` | Comma-separated list of your domain(s) |
| `DB_ENGINE` | `django.db.backends.mysql` for MySQL |
| `DB_NAME` | Database name |
| `DB_USER` | Database user |
| `DB_PASSWORD` | Database password |
| `DB_HOST` | Database host |
| `DB_PORT` | Database port (default 3306) |

### Deploy on Railway / Render / Heroku

1. Push your code to GitHub
2. Connect the repo on your hosting platform
3. Set the environment variables above
4. The `Procfile` handles starting gunicorn and running migrations automatically

---

## Default Roles

Run the setup script to create default accounts:

```bash
python scripts/create_default_accounts.py
```

---

## License

© 2026 AbleGod College. All rights reserved.  
**Developed by BG DevOps — 0784654328**
