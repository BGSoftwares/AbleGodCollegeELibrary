# AbleGod College E-Library

A Django-based college e-library for discovering, reading, downloading and managing educational resources such as textbooks, notes and past examination papers.

## Technology

- Python / Django
- SQLite by default (development and current low-cost deployment)
- MySQL remains supported for future migration
- HTML / CSS / Bootstrap
- WhiteNoise for production static files
- Gunicorn for production WSGI serving

## Local setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Production configuration

Set these environment variables on the hosting platform:

```text
SECRET_KEY=<strong-random-secret>
DEBUG=False
ALLOWED_HOSTS=<your-domain>
CSRF_TRUSTED_ORIGINS=https://<your-domain>
SECURE_SSL_REDIRECT=True
```

SQLite remains the default database. For a free deployment, the hosting provider must provide **persistent disk storage** for `db.sqlite3` and the `media/` directory. Without persistent storage, database records and uploaded books can be lost when the service is rebuilt or redeployed.

The application health endpoint is:

```text
/health/
```

It performs a database check and returns HTTP 200 when the application and database are healthy.

## Production process

The included `Procfile` uses Gunicorn and runs migrations during the release phase:

```text
web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate
```

## Important SQLite limitation

SQLite is intentionally being kept for the current deployment because it avoids external database costs and preserves the existing application with minimal change. It is suitable for a small-to-moderate college library, but it is not the long-term choice for heavy concurrent writes or multiple application instances. When the library grows, migrate to PostgreSQL using Django migrations and a database backup rather than changing the application's business logic.

## Security

Never commit `.env`, real credentials, database passwords or secret keys. Configure secrets through the hosting platform.
