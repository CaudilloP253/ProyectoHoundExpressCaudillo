"""
Django settings for hello project.
"""

import os
import socket
import sys
from pathlib import Path
from distutils.util import strtobool

# ------------------------------------------------------------------------------
# PATHS
# ------------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent  # /app/src
PROJECT_ROOT = BASE_DIR.parent  # /app

# ------------------------------------------------------------------------------
# SECURITY
# ------------------------------------------------------------------------------

SECRET_KEY = os.environ.get("SECRET_KEY", "unsafe-dev-key")

DEBUG = bool(strtobool(os.getenv("DEBUG", "false")))

TESTING = "test" in sys.argv

allowed_hosts = os.getenv("ALLOWED_HOSTS", ".localhost,127.0.0.1,[::1]")
ALLOWED_HOSTS = list(map(str.strip, allowed_hosts.split(",")))

# ------------------------------------------------------------------------------
# APPLICATIONS
# ------------------------------------------------------------------------------

INSTALLED_APPS = [
    "pages.apps.PagesConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

if DEBUG and not TESTING:
    INSTALLED_APPS += ["debug_toolbar"]

# ------------------------------------------------------------------------------
# MIDDLEWARE
# ------------------------------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG and not TESTING:
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

# ------------------------------------------------------------------------------
# URLS / WSGI
# ------------------------------------------------------------------------------

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# ------------------------------------------------------------------------------
# TEMPLATES
# ------------------------------------------------------------------------------

default_loaders = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

cached_loaders = [("django.template.loaders.cached.Loader", default_loaders)]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_ROOT / "templates"],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": default_loaders if DEBUG else cached_loaders,
        },
    },
]

# ------------------------------------------------------------------------------
# DATABASE (Docker Postgres)
# ------------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("DB_HOST", "db"),
        "PORT": os.environ.get("DB_PORT", 5432),
    }
}

# ------------------------------------------------------------------------------
# PASSWORD VALIDATION
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ------------------------------------------------------------------------------
# SESSIONS
# ------------------------------------------------------------------------------

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

# ------------------------------------------------------------------------------
# REDIS / CACHE / CELERY
# ------------------------------------------------------------------------------

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    }
}

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

# ------------------------------------------------------------------------------
# INTERNATIONALIZATION
# ------------------------------------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------------------
# STATIC FILES (CORREGIDO PARA DOCKER)
# ------------------------------------------------------------------------------

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    PROJECT_ROOT / "public",
]

STATIC_ROOT = PROJECT_ROOT / "public_collected"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ------------------------------------------------------------------------------
# DEBUG TOOLBAR
# ------------------------------------------------------------------------------

if DEBUG:
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [
        ip[: ip.rfind(".")] + ".1" for ip in ips
    ] + ["127.0.0.1", "10.0.2.2"]
