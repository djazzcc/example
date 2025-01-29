# -------------------------
# Djazz Production Settings
#
# This module contains Django settings specific to the production environment.
# All sensitive values and environment-specific configurations must be defined
# in the .env file for security purposes.
#
# Important:
#   - Default values from base.py are not allowed in production
#   - All critical settings must be explicitly defined in .env
#   - Never commit sensitive values directly in this file
#   - Never stage or commit .env file to the repository
#
# For more information on deployment best practices, see:
# https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
# -------------------------

from .base import *  # noqa
from email.utils import getaddresses


# https://docs.djangoproject.com/en/5.1/ref/settings/#admins 
# Example (in .env): ADMINS=John Doe <john@example.com>,Jane Doe <jane@example.com>
ADMINS = getaddresses([env('ADMINS')])

# https://docs.djangoproject.com/en/5.1/ref/settings/#allowed-hosts
# Example (in .env): ALLOWED_HOSTS=example.com,www.example.com
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])

# https://docs.djangoproject.com/en/5.1/ref/settings/#caches
# Example (in .env): CACHE_URL=redis://redis:6379/1
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('CACHE_URL'),
        'OPTIONS': {
            'COMPRESSOR': "django_redis.compressors.zlib.ZlibCompressor",
            'COMPRESS_MIN_LEN': 1024,  # Compress only values larger than 1KB
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
}

# https://docs.djangoproject.com/en/5.1/ref/settings/#databases 
# Example (in .env): DATABASE_URL=postgres://username:password@host:port/database_name
DATABASES = {
    "default": env.db("DATABASE_URL")
}

# https://docs.djangoproject.com/en/5.1/ref/settings/#debug
# Debug should be strictly False in production
DEBUG = env.bool("DJANGO_DEBUG", False)

# https://docs.djangoproject.com/en/5.1/ref/settings/#default-from-email
# Example (in .env): DEFAULT_FROM_EMAIL="Djazz! <info@example.com>"
DEFAULT_FROM_EMAIL = "noreply@example.com"

# https://docs.djangoproject.com/en/5.1/ref/settings/#email-backend
# https://anymail.dev/en/stable/
# Example (in .env): EMAIL_BACKEND="anymail.backends.brevo.EmailBackend"
# Example (in .env): BREVO_API_KEY="your_brevo_api_key"
# You can use anymail to send emails from your Django app, check anymail docs
# for more information.
EMAIL_BACKEND = "anymail.backends.brevo.EmailBackend"
ANYMAIL = {
    "BREVO_API_KEY": env("BREVO_API_KEY"),
    "BREVO_API_URL": env("BREVO_API_URL", default="https://api.brevo.com/v3/"),
}

# https://docs.djangoproject.com/en/5.1/ref/settings/#email-subject-prefix
# Example (in .env): EMAIL_SUBJECT_PREFIX="[Djazz] "
EMAIL_SUBJECT_PREFIX = env("EMAIL_SUBJECT_PREFIX")

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
    CORE_DIR / 'static',
]

# Use the default static files storage instead of ManifestStaticFilesStorage
# Remove or comment out this line:
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Add proper MIME type mapping
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Add security headers but don't interfere with static files
SECURE_CONTENT_TYPE_NOSNIFF = False  # Temporarily disable for debugging

# Secret key
SECRET_KEY = env("SECRET_KEY")

# Disable debug toolbar
INSTALLED_APPS = [app for app in INSTALLED_APPS if not app.startswith('debug_toolbar')]
MIDDLEWARE = [m for m in MIDDLEWARE if not m.startswith('debug_toolbar')]

