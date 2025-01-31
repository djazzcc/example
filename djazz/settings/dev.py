# --------------------------
# Djazz Development Settings
#
# This module contains Django settings specific to the development environment.
# It extends base.py with development-specific configurations such as:
#   - Debug toolbar
#   - Local database settings
#   - Development-specific apps
#   - Relaxed security settings
#
# Note:
#   - These settings are NOT suitable for production use
#   - Debug mode is enabled by default
#   - Security features may be disabled for development convenience
# ---------------------------

from .base import *         
from .base import INSTALLED_APPS
from .base import MIDDLEWARE
from .base import CACHE_URL 
from .base import DATABASE_URL
from socket import gethostname, gethostbyname, gethostbyname_ex

# https://docs.djangoproject.com/en/5.1/ref/settings/#allowed-hosts
# https://stackoverflow.com/a/40665906 
ALLOWED_HOSTS = ['.localhost','.local', '127.0.0.1', '[::1]']
ALLOWED_HOSTS += [ gethostname(), ] + list(set(gethostbyname_ex(gethostname())[2]))

if CACHE_URL is not None:
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
if DATABASE_URL is not None:
    DATABASES = {
        "default": env.db("DATABASE_URL")
    }

# https://docs.djangoproject.com/en/5.1/ref/settings/#debug
DEBUG = True

# Django Debug Toolbar
# https://django-debug-toolbar.readthedocs.io/en/latest/index.html
INSTALLED_APPS += ["debug_toolbar"]

# https://docs.djangoproject.com/en/dev/ref/settings/#internal-ips
INTERNAL_IPS = ["127.0.0.1", "::1"]
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#add-the-debug-toolbar-middleware
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
