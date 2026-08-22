import os
from pathlib import Path

from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured

# ---------------------------------------------------------------------------
# BASE DIRECTORY
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# ENVIRONMENT VARIABLES
# ---------------------------------------------------------------------------
# Load the project .env file if it exists.
#
# On PythonAnywhere, you can also keep your production secrets in:
# /home/BGDevopps/.ablegod.env
# ---------------------------------------------------------------------------

PROJECT_ENV = BASE_DIR / ".env"
PYTHONANYWHERE_ENV = Path("/home/BGDevopps/.ablegod.env")

if PYTHONANYWHERE_ENV.exists():
    load_dotenv(PYTHONANYWHERE_ENV)

if PROJECT_ENV.exists():
    load_dotenv(PROJECT_ENV)


# ---------------------------------------------------------------------------
# SECURITY
# ---------------------------------------------------------------------------

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "django-insecure-development-only-key"
    else:
        raise ImproperlyConfigured(
            "SECRET_KEY must be set when DEBUG=False."
        )


# ---------------------------------------------------------------------------
# ALLOWED HOSTS
# ---------------------------------------------------------------------------

_allowed_hosts = os.getenv("ALLOWED_HOSTS", "")

if _allowed_hosts:
    ALLOWED_HOSTS = [
        host.strip()
        for host in _allowed_hosts.split(",")
        if host.strip()
    ]
else:
    ALLOWED_HOSTS = [
        "127.0.0.1",
        "localhost",
        "BGDevopps.pythonanywhere.com",
    ]


# ---------------------------------------------------------------------------
# APPLICATIONS
# ---------------------------------------------------------------------------

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "bootstrap5",

    # Local apps
    "accounts",
    "books",
]


# ---------------------------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise for static files
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ---------------------------------------------------------------------------
# URL CONFIGURATION
# ---------------------------------------------------------------------------

ROOT_URLCONF = "config.urls"


# ---------------------------------------------------------------------------
# TEMPLATES
# ---------------------------------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ---------------------------------------------------------------------------
# WSGI
# ---------------------------------------------------------------------------

WSGI_APPLICATION = "config.wsgi.application"


# ---------------------------------------------------------------------------
# DATABASE
# ---------------------------------------------------------------------------

DATABASE_ENGINE = os.getenv("DATABASE_ENGINE", "mysql").lower()


if DATABASE_ENGINE == "sqlite":

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


else:

    # PyMySQL is used as the MySQL driver.
    import pymysql

    pymysql.install_as_MySQLdb()

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",

            "NAME": os.getenv(
                "DB_NAME",
                "ablegod_elibrary",
            ),

            "USER": os.getenv(
                "DB_USER",
                "ablegod_user",
            ),

            "PASSWORD": os.getenv(
                "DB_PASSWORD",
                "",
            ),

            "HOST": os.getenv(
                "DB_HOST",
                "127.0.0.1",
            ),

            "PORT": os.getenv(
                "DB_PORT",
                "3306",
            ),

            "OPTIONS": {
                "charset": "utf8mb4",
            },

            "CONN_MAX_AGE": 60,
        }
    }


# ---------------------------------------------------------------------------
# PASSWORD VALIDATION
# ---------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# ---------------------------------------------------------------------------
# INTERNATIONALIZATION
# ---------------------------------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Harare"

USE_I18N = True

USE_TZ = True


# ---------------------------------------------------------------------------
# STATIC FILES
# ---------------------------------------------------------------------------

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# ---------------------------------------------------------------------------
# WHITE NOISE
# ---------------------------------------------------------------------------

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },

    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage."
            "CompressedManifestStaticFilesStorage"
        ),
    },
}


# ---------------------------------------------------------------------------
# MEDIA FILES
# ---------------------------------------------------------------------------

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ---------------------------------------------------------------------------
# AUTHENTICATION
# ---------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.User"

LOGIN_REDIRECT_URL = "dashboard"

LOGIN_URL = "login"

LOGOUT_REDIRECT_URL = "login"


# ---------------------------------------------------------------------------
# SECURITY SETTINGS
# ---------------------------------------------------------------------------

if not DEBUG:

    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )

    SECURE_SSL_REDIRECT = (
        os.getenv(
            "SECURE_SSL_REDIRECT",
            "True",
        ).lower()
        == "true"
    )

    SECURE_BROWSER_XSS_FILTER = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

    SECURE_REFERRER_POLICY = "same-origin"

    X_FRAME_OPTIONS = "DENY"

    SECURE_HSTS_SECONDS = 31536000

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_HSTS_PRELOAD = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True


# ---------------------------------------------------------------------------
# CSRF TRUSTED ORIGINS
# ---------------------------------------------------------------------------

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CSRF_TRUSTED_ORIGINS",
        "https://BGDevopps.pythonanywhere.com",
    ).split(",")
    if origin.strip()
]


# ---------------------------------------------------------------------------
# DEFAULT FIELD
# ---------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
