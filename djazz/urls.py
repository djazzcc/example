
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
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from core.search import views as search_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
]

if settings.DEBUG:
    import debug_toolbar  # noqa

    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
        path('404/', TemplateView.as_view(template_name='404.html')),
        path('500/', TemplateView.as_view(template_name='500.html')),
        path('403/', TemplateView.as_view(template_name='403.html')),
        path('403-csrf/', TemplateView.as_view(template_name='403_csrf.html')),
    ]

urlpatterns += i18n_patterns(
    path('search/', search_views.search, name='search'),
    # Any other URL patterns should be added here, BEFORE the wagtail_urls.
    path('', include(wagtail_urls)),
)