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
from core.utils.views import WelcomeView

# Enable i18n only if both Django and Wagtail i18n are enabled
I18N_ENABLED = settings.USE_I18N and settings.WAGTAIL_I18N_ENABLED

# Base URL patterns that don't need i18nU
urlpatterns = [
    # TODO: Remove this temporary welcome page and replace with your own URLs
    path('', WelcomeView.as_view(), name='welcome'),  # Delete this line after setting up your own homepage
    
    path('admin/', admin.site.urls),
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
]

# Debug-only patterns
if settings.DEBUG:
    import debug_toolbar  # noqa

    # Add debug toolbar URLs
    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]

    # Add debug template preview URLs
    debug_urlpatterns = (
        path('404/', TemplateView.as_view(template_name='404.html')),
        path('500/', TemplateView.as_view(template_name='500.html')),
        path('403/', TemplateView.as_view(template_name='403.html')),
        path('403-csrf/', TemplateView.as_view(template_name='403_csrf.html')),
    )
    
    urlpatterns += i18n_patterns(*debug_urlpatterns) if I18N_ENABLED else debug_urlpatterns

# Main URL patterns that might need i18n
# Place your main URL patterns here, before wagtail_urls
main_urlpatterns = (
    path('search/', search_views.search, name='search'),
    path('users/', include('core.users.urls')),
    # Any other URL patterns should be added here, BEFORE the wagtail_urls.
    path('', include(wagtail_urls)),
)

# Add main patterns with i18n if enabled
urlpatterns += i18n_patterns(*main_urlpatterns) if I18N_ENABLED else main_urlpatterns