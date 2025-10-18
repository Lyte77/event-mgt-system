# settings/prod.py

from .settings import *
import environ

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")  # Load environment variables

# ---------------------------------------------
# GENERAL CONFIG
# ---------------------------------------------
DEBUG = False

ALLOWED_HOSTS = [
    "your-pythonanywhere-username.pythonanywhere.com",  # example
    "www.yourcustomdomain.com",  # if you add a domain later
]

# ---------------------------------------------
# SECURITY SETTINGS
# ---------------------------------------------
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True

# ---------------------------------------------
# DATABASE (Postgres on Render)
# ---------------------------------------------
DATABASES = {
    'default': env.db('DATABASE_URL', default=''),
}

# ---------------------------------------------
# STATIC & MEDIA FILES
# ---------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles'

# ---------------------------------------------
# EMAIL (Production-ready)
# ---------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ---------------------------------------------
# LOGGING
# ---------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/django_error.log',
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'WARNING',
    },
}

# ---------------------------------------------
# ALLOWED HOSTS CHECK
# ---------------------------------------------
if not ALLOWED_HOSTS:
    raise Exception("⚠️ ALLOWED_HOSTS must be set in production settings")
