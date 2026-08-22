from pathlib import Path
import os

from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured


# ============================================================================
# BASE DIRECTORY
# ============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================================
# ENVIRONMENT VARIABLES
# ============================================================================

# Production environment file on PythonAnywhere
PYTHONANYWHERE_ENV = Path("/home/BGDevopps/.ablegod.env")

if PYTHONANYWHERE_ENV.exists():
    load_dotenv(PYTHONANYWHERE_ENV)

# Local development .env
PROJECT_ENV = BASE_DIR / ".env"

if PROJECT_ENV.exists():
    load_dotenv(PROJECT_ENV)


# ============================================================================
# SECURITY
# ============================================================================

DEBUG = os.getenv("DEBUG", "False").strip().lower() == "true"


SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "django-insecure-development-only-key"
    else:
        raise ImproperlyConfigured(
            "SECRET_KEY must be set when DEBUG=False."
        )


# ============================================================================
# ALLOWED HOSTS
# ============================================================================

_allowed_hosts = os.getenv("ALLOWED_HOSTS", "").strip()

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


# ============================================================================
# CSRF
# ============================================================================

_csrf_origins = os.getenv("CSRF_TRUSTED_ORIGINS", "").strip()

if _csrf_origins:
    CSRF_TRUSTED_ORIGINS = [
        origin.strip()
        for origin in _csrf_origins.split(",")
        if origin.strip()
    ]
else:
    CSRF_TRUSTED_ORIGINS = [
        "https://BGDevopps.pythonanywhere.com",
    ]


# ============================================================================
# APPLICATIONS
# ============================================================================

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "django_bootstrap5",

    # Local applications
    "accounts",
    "books",
    "categories",
    "authors",
    "publishers",
    "departments",
    "borrowing",
    "notifications",
    "dashboard",
]


# ============================================================================
# MIDDLEWARE
# ============================================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # Static file serving
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================================
# URL CONFIGURATION
# ============================================================================

ROOT_URLCONF = "config.urls"


# ============================================================================
# TEMPLATES
# ============================================================================

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


# ============================================================================
# WSGI
# ============================================================================

WSGI_APPLICATION = "config.wsgi.application"


# ============================================================================
# DATABASE
# ============================================================================
#
# SQLite ONLY.
#
# IMPORTANT:
# There is intentionally NO pymysql import here.
# There is intentionally NO MySQL configuration here.
#
# This prevents an old .env variable such as DATABASE_ENGINE=mysql
# from accidentally switching the deployment back to MySQL.
#

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "OPTIONS": {
            "timeout": 30,
        },
    }
}


# ============================================================================
# PASSWORD VALIDATION
# ============================================================================

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


# ============================================================================
# INTERNATIONALIZATION
# ============================================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Harare"

USE_I18N = True

USE_TZ = True


# ============================================================================
# STATIC FILES
# ============================================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# ============================================================================
# STATIC STORAGE / WHITENOISE
# ============================================================================

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },

    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage.CompressedManifestStaticFilesStorage"
        ),
    },
}


# ============================================================================
# MEDIA FILES
# ============================================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ============================================================================
# AUTHENTICATION
# ============================================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.User"

LOGIN_REDIRECT_URL = "dashboard"

LOGIN_URL = "login"

LOGOUT_REDIRECT_URL = "login"


# ============================================================================
# PRODUCTION SECURITY
# ============================================================================

if not DEBUG:

    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )

    SECURE_SSL_REDIRECT = (
        os.getenv(
            "SECURE_SSL_REDIRECT",
            "True",
        ).strip().lower()
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
