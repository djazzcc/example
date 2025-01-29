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

# https://docs.djangoproject.com/en/5.1/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.localhost','.local', '127.0.0.1', '[::1]']

# https://docs.djangoproject.com/en/5.1/ref/settings/#debug
DEBUG = True

# https://docs.djangoproject.com/en/5.1/ref/settings/#email-backend
# Write email to console in development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Django Debug Toolbar
# https://django-debug-toolbar.readthedocs.io/en/latest/index.html
INSTALLED_APPS += ["debug_toolbar"]

# https://docs.djangoproject.com/en/dev/ref/settings/#internal-ips
INTERNAL_IPS = ["127.0.0.1", "::1"]
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#add-the-debug-toolbar-middleware
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
