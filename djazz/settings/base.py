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
# Base settings for Djazz
# This file is used to configure the Django settings for the base environment.
# It is best practice to not change the settings in this file.
# Instead, you should check dev.py, test.py, and production.py for the settings.
# Settings are seperated to diffrent sections, inside each section, sorted alphabetically.
#   1. Django Core settings
#   2. Django `Auth` settings
#   3. Django `Messages` settings
#   4. Django `Sessions` settings
#   5. Django `Sites` settings
#   6. Django `Static Files` settings
#   7. Wagtail settings
#   8. Celery settings
# Try to use the Numbers to find the settings you need with Ctrl(CMD)+F in your IDE.
# ----------------------------

from pathlib import Path
import environ  
from django.utils.translation import gettext_lazy as _
from django.contrib.messages import constants as messages


BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_DIR = BASE_DIR / "djazz"
CORE_DIR = BASE_DIR / "core"

# ----
# .ENV
# ----
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

# -----------------------
# 1. Django Core settings
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
CACHE_URL = env.str("CACHE_URL", default=None)
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
DATABASE_URL = env.db("DATABASE_URL", default=None)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR/ "db.sqlite3"
    }
}

# https://docs.djangoproject.com/en/5.1/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)

# https://docs.djangoproject.com/en/5.1/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL", default="Djazz! <info@example.com>")

# https://docs.djangoproject.com/en/5.1/ref/settings/#email-backend
EMAIL_BACKEND = env.str("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")

# https://docs.djangoproject.com/en/5.1/ref/settings/#email-host 
EMAIL_HOST = env.str("EMAIL_HOST", default="localhost")

# https://docs.djangoproject.com/en/5.1/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", default="")

# https://docs.djangoproject.com/en/5.1/ref/settings/#email-host-user
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", default="")

# https://docs.djangoproject.com/en/5.1/ref/settings/#email-port
EMAIL_PORT = env.int("EMAIL_PORT", default=25)

# https://docs.djangoproject.com/en/5.1/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = "[Djazz] "

# https://docs.djangoproject.com/en/5.1/ref/settings/#fixture-dirs
FIXTURE_DIRS = CORE_DIR / "fixtures"

# https://docs.djangoproject.com/en/5.1/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.DjangoTemplates"

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
# Order of apps is important, applications listed first has precedence over
# the ones listed later. So if you want to override a app, place yours before
# the ones you want to override.

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

WAGTAIL_APPS = [
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
]

THIRD_PARTY_APPS = [
    "modelcluster",
    "taggit",
    "django_celery_results",
    "django_celery_beat",
]

CORE_APPS = [
    "core.utils",
    "core.search",
    "core.users",
]

# Place your apps here. Remember the order of apps is important.
LOCAL_APPS = [
    # Add your apps here. Example: "apps.your_app"
]

# DO NOT CHANGE THIS ORDER
INSTALLED_APPS = LOCAL_APPS + WAGTAIL_APPS + THIRD_PARTY_APPS + CORE_APPS + DJANGO_APPS

# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"

# https://docs.djangoproject.com/en/dev/ref/settings/#languages
LANGUAGES = [
    ("en", _("English")),
]

# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [
    CORE_DIR / "locale",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'core.utils.templatetags.vite': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = BASE_DIR / "media"

# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# https://docs.djangoproject.com/en/5.1/ref/settings/#middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

# https://docs.djangoproject.com/en/5.1/ref/settings/#root-urlconf
ROOT_URLCONF = "djazz.urls"

# https://docs.djangoproject.com/en/5.1/ref/settings/#secret-key
SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="djazz-secret-key")

# https://docs.djangoproject.com/en/5.1/ref/settings/#server-email
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# https://docs.djangoproject.com/en/5.1/ref/settings/#storages
# This values are used for the default storage backend,
# If you are using S3, you can change the values to use the S3 storage backend
# or use the custom storage backend, keep this unchanged and change the values
# in the dev.py or production.py file.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# https://docs.djangoproject.com/en/5.1/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [CORE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# https://docs.djangoproject.com/en/5.1/ref/settings/#std-setting-TIME_ZONE
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# Keep this as UTC, it is used for the default timezone. change yours in the 
# dev.py or production.py file.
TIME_ZONE = "UTC"

# https://docs.djangoproject.com/en/5.1/ref/settings/#use-i18n
USE_I18N = True

# https://docs.djangoproject.com/en/5.1/ref/settings/#use-tz
USE_TZ = True

# https://docs.djangoproject.com/en/5.1/ref/settings/#wsgi-application
# This is the WSGI application used by Django, you don't need to change this.
WSGI_APPLICATION = "djazz.wsgi.application"

# https://docs.djangoproject.com/en/5.1/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# -----------------------
# 2. Django `Auth` settings
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth
# --------------------

# https://docs.djangoproject.com/en/5.1/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-user-model
AUTH_USER_MODEL = 'users.User'

# https://docs.djangoproject.com/en/5.1/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "users:profile"

# https://docs.djangoproject.com/en/5.1/ref/settings/#login-url
LOGIN_URL = "users:login"

# https://docs.djangoproject.com/en/5.1/ref/settings/#logout-redirect-url
LOGOUT_REDIRECT_URL = "users:login"

# https://docs.djangoproject.com/en/5.1/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

# https://docs.djangoproject.com/en/5.1/ref/settings/#password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------------
# 3. Django `Messages` settings
# https://docs.djangoproject.com/en/5.1/ref/settings/#messages
# -----------------------------

# https://docs.djangoproject.com/en/5.1/ref/settings/#messages-storage
# Try session storage first, if it fails, use fallback to cookie storage.
MESSAGE_STORAGE = "django.contrib.messages.storage.fallback.FallbackStorage"

# https://docs.djangoproject.com/en/5.1/ref/settings/#messages-tags
# Make it sync with bootstrap alert classes
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}


# -----------------------------
# 4. Django `Sessions` settings
# https://docs.djangoproject.com/en/5.1/ref/settings/#sessions
# -----------------------------

# https://docs.djangoproject.com/en/5.1/ref/settings/#session-engine
SESSION_ENGINE = "django.contrib.sessions.backends.cache"


# --------------------------
# 5. Django `Sites` settings
# https://docs.djangoproject.com/en/5.1/ref/settings/#sites
# -------------------------

SITE_ID = 1


# ---------------------------------
# 6. Django `Static Files` settings
# https://docs.djangoproject.com/en/5.1/ref/settings/#static-files
# ---------------------------------

# https://docs.djangoproject.com/en/5.1/ref/settings/#static-root
# This is the directory where the static files will be collected.
STATIC_ROOT = BASE_DIR / "static"

# https://docs.djangoproject.com/en/5.1/ref/settings/#static-url
STATIC_URL = "/static/"

# https://docs.djangoproject.com/en/5.1/ref/settings/#static-files-dir
STATICFILES_DIRS = [
    CORE_DIR / "static",
]

# https://docs.djangoproject.com/en/5.1/ref/settings/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# -------------------
# 7. Wagtail settings
# https://docs.wagtail.org/en/stable/reference/settings.html
# ---------------------------------

# https://docs.wagtail.org/en/stable/reference/settings.html#wagtail-site-name 
# You might want to change this to your project name.
WAGTAIL_SITE_NAME = "Djazz CMS"

# https://docs.wagtail.org/en/stable/reference/settings.html#wagtailadmin-base-url 
# Example: https://example.com
WAGTAILADMIN_BASE_URL = "http://localhost:8000"

# https://docs.wagtail.org/en/stable/reference/settings.html#wagtail-i18n-enabled
WAGTAIL_I18N_ENABLED = False

# https://docs.wagtail.org/en/stable/reference/settings.html#wagtail-content-languages
WAGTAIL_CONTENT_LANGUAGES = LANGUAGES

# https://docs.wagtail.org/en/stable/reference/settings.html#wagtail-locale-path
WAGTAIL_LOCALE_PATH = CORE_DIR / "locale"

# https://docs.wagtail.org/en/stable/reference/settings.html#wagtailembeds-responsive-html
# TODO: This needs some additional setup on the frontend.
WAGTAILEMBEDS_RESPONSIVE_HTML = True

# https://docs.wagtail.org/en/stable/reference/settings.html#wagtailimages-max-upload-size
WAGTAILIMAGES_MAX_UPLOAD_SIZE = 20 * 1024 * 1024  # 20MB 

# https://docs.wagtail.org/en/stable/reference/settings.html#wagtailimages-extensions
WAGTAILIMAGES_EXTENSIONS = ["gif", "jpg", "jpeg", "png", "webp"]

# https://docs.wagtail.org/en/stable/reference/settings.html#wagtailimages-rendition-opts
WAGTAILIMAGES_RENDER_FORMATS = ["webp"]

# https://docs.wagtail.org/en/stable/reference/settings.html#wagtail-enable-update-check
WAGTAIL_ENABLE_UPDATE_CHECK = False

# https://docs.wagtail.org/en/stable/reference/settings.html#wagtail-password-required-template 
WAGTAIL_PASSWORD_REQUIRED_TEMPLATE = 'myapp/password_required.html'

# https://docs.wagtail.org/en/stable/reference/settings.html#wagtail-workflow-enabled
# This is for saving memory, if you need wagtail workflow, set this to True.
WAGTAIL_WORKFLOW_ENABLED = False


# -----------------------------
# 8. Celery settings
# https://docs.celeryq.dev/en/stable/userguide/configuration.html
# -----------------------------

# Redis URL for Celery
REDIS_URL = env.str('REDIS_URL', default='redis://localhost:6379/1')

# Celery Configuration Options
CELERY_ACCEPT_CONTENT = ['json']
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_BROKER_URL = REDIS_URL

# Result Backend Settings
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True
CELERY_RESULT_BACKEND_MAX_RETRIES = 3
CELERY_RESULT_EXTENDED = True
CELERY_RESULT_SERIALIZER = 'json'

# Task Settings
CELERY_TASK_SEND_SENT_EVENT = True
CELERY_TASK_SERIALIZER = 'json'
CELERY_TASK_SOFT_TIME_LIMIT = 60
CELERY_TASK_TIME_LIMIT = 5 * 60
CELERY_TASK_TRACK_STARTED = True

# General Settings
CELERY_TIMEZONE = TIME_ZONE
CELERY_WORKER_SEND_TASK_EVENTS = True