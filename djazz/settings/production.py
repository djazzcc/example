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