import sys
import django
from django.views.generic import TemplateView
from django.conf import settings

class WelcomeView(TemplateView):
    template_name = "utils/welcome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'django_version': django.get_version(),
            'python_version': sys.version.split()[0],
            'installed_apps': [app.split('.')[-1] for app in settings.INSTALLED_APPS],
        })
        return context 