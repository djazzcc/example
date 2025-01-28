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

from .base import * 
from email.utils import getaddresses


# https://docs.djangoproject.com/en/5.1/ref/settings/#admins 
# Example (in .env): ADMINS=John Doe <john@example.com>,Jane Doe <jane@example.com>
ADMINS = getaddresses([env('ADMINS')])

# https://docs.djangoproject.com/en/5.1/ref/settings/#allowed-hosts
# Example (in .env): ALLOWED_HOSTS=example.com,www.example.com
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

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
    'default': env.db(),
}

# https://docs.djangoproject.com/en/5.1/ref/settings/#debug
# Debug should be strictly False in production
DEBUG = False

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

