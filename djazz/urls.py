
# djazz/urls.py
# ----------------------
# Root URL configuration
# https://docs.djangoproject.com/en/dev/topics/http/urls/
# https://docs.djangoproject.com/en/5.0/topics/i18n/translation/#the-set-language-redirect-view
# https://docs.wagtail.org/en/stable/advanced_topics/i18n.html#adding-a-language-prefix-to-urls
# ----------------------
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar  # noqa

    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]