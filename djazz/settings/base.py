# ----------------------------
#      _  _                  
#     | |(_)                 
#   __| | _   __ _  ____ ____
#  / _` || | / _` ||_  /|_  /
# | (_| || || (_| | / /  / / 
#  \__,_|| | \__,_|/___|/___|
#       _/ |                 
#      |__/                  
#      @azataiot - 2025 
# ----------------------------

from pathlib import Path
import environ  


BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_DIR = BASE_DIR / "djazz"
CORE_DIR = PROJECT_DIR / "core"

# ----
# .ENV
# ----
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

# --------------------
# Django Core settings
# https://docs.djangoproject.com/en/5.1/ref/settings/#core-settings
# --------------------

# https://docs.djangoproject.com/en/5.1/ref/settings/#admins 
ADMINS = []

# https://docs.djangoproject.com/en/5.1/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# https://docs.djangoproject.com/en/5.1/ref/settings/#append-slash
# Requires: 'django.middleware.common.CommonMiddleware', enabled by default
APPEND_SLASH = True

# https://docs.djangoproject.com/en/5.1/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# https://docs.djangoproject.com/en/5.1/ref/settings/#csrf-cookie-httponly
# TODO: Research this later.
CSRF_COOKIE_HTTPONLY = False

# https://docs.djangoproject.com/en/5.1/ref/settings/#csrf-cookie-name
CSRF_COOKIE_NAME = "djazz-csrftoken"
# https://docs.djangoproject.com/en/5.1/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = False

# https://docs.djangoproject.com/en/5.1/ref/settings/#databases 
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR/ "db.sqlite3"
    }
}

# https://docs.djangoproject.com/en/5.1/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)

# https://docs.djangoproject.com/en/5.1/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = "noreply@example.com"