from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
import json

register = template.Library()

@register.simple_tag
def vite_asset(path):
    """
    Resolve a Vite asset path based on manifest.json in development and production.
    """
    if settings.DEBUG:
        return f'http://localhost:5173/static/{path}'
    
    try:
        manifest_path = settings.STATIC_ROOT / 'manifest.json'
        with open(manifest_path) as f:
            manifest = json.load(f)
    except FileNotFoundError:
        return f'/static/{path}'
    
    try:
        return f'/static/{manifest[path]["file"]}'
    except KeyError:
        return f'/static/{path}'

@register.simple_tag
def vite_hmr():
    """
    Include Vite HMR script in development.
    """
    if settings.DEBUG:
        return mark_safe(
            '<script type="module" src="http://localhost:5173/@vite/client"></script>'
        )
    return '' 