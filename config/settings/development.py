# eventapp/settings/dev.py
from .settings import *   # import everything from base
import os

# -----------------------------------------------------------------------------
# Debug / Hosts
# -----------------------------------------------------------------------------
DEBUG = True

# In dev we allow localhost and the machine hostname
ALLOWED_HOSTS = ["127.0.0.1", "localhost",  "event-mgt-system.onrender.com"]

# -----------------------------------------------------------------------------
# Secret key (dev fallback)
# -----------------------------------------------------------------------------
# base.py already reads SECRET_KEY from env; allow a dev fallback here if needed
SECRET_KEY = env("SECRET_KEY")

# -----------------------------------------------------------------------------
# Database - local sqlite by default (easy, zero config)
# -----------------------------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# -----------------------------------------------------------------------------
# Static & media - local convenience
# -----------------------------------------------------------------------------
# STATICFILES_DIRS is defined in base; keep collectstatic behavior but serve locally
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# -----------------------------------------------------------------------------
# Email - use console backend in development
# -----------------------------------------------------------------------------
EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="dev@example.com")

# -----------------------------------------------------------------------------
# Django Debug Toolbar (optional but highly recommended for dev)
# -----------------------------------------------------------------------------
# install: pip install django-debug-toolbar
if env.bool("ENABLE_DEBUG_TOOLBAR", default=True):
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

    # Allow toolbar on local addresses
    INTERNAL_IPS = ["127.0.0.1", "localhost"]

    # Simple function to show toolbar in some containerized setups
    # INTERNAL_IPS = type(os.getenv("INTERNAL_IPS"), (list,), {})(os.getenv("INTERNAL_IPS", "127.0.0.1").split(","))

# -----------------------------------------------------------------------------
# Logging - verbose for local debugging
# -----------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {"handlers": ["console"], "level": "DEBUG"},
    "loggers": {
        "allauth": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}

# -----------------------------------------------------------------------------
# Other dev conveniences
# -----------------------------------------------------------------------------
# Allow template debug (useful for error pages to show template source)
TEMPLATES[0]["OPTIONS"]["debug"] = True

# SESSION / CSRF cookies are not forced to secure in dev
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# If you run tailwind with django-tailwind locally, you may want to set:
# TAILWIND_DEV_MODE = True   # if you use django-tailwind and want its dev server
