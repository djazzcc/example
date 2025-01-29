from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
import json
import shutil
from pathlib import Path

register = template.Library()

def ensure_manifest_exists():
    """
    Ensure manifest.json exists in the static directory by copying it from .vite
    """
    if not settings.DEBUG:
        source = settings.CORE_DIR / 'static/.vite/manifest.json'
        dest = settings.STATIC_ROOT / '.vite'
        
        if source.exists():
            # Create .vite directory if it doesn't exist
            dest.mkdir(exist_ok=True)
            # Copy manifest.json
            shutil.copy2(source, dest / 'manifest.json')

@register.simple_tag
def vite_asset(path):
    """
    Resolve a Vite asset path based on manifest.json in development and production.
    """
    if settings.DEBUG:
        return f'http://127.0.0.1:3000/{path}'
    
    try:
        # Ensure manifest exists in static directory
        ensure_manifest_exists()
        
        manifest_path = settings.STATIC_ROOT / '.vite/manifest.json'
        with open(manifest_path) as f:
            manifest = json.load(f)

        entry_point = manifest["core/assets/js/main.js"]
        
        if path == 'css/main.css':
            # Get the hashed CSS filename from the entry's css array
            return f'/static/{entry_point["css"][0]}'
        elif path == 'js/main.js':
            # Get the hashed JS filename
            return f'/static/{entry_point["file"]}'
        
        # Handle other assets
        return f'/static/{manifest[path]["file"]}'
    except (FileNotFoundError, KeyError) as e:
        return f'/static/{path}'

@register.simple_tag
def vite_hmr():
    """
    Include Vite HMR script in development.
    """
    if settings.DEBUG:
        return mark_safe(
            '<script type="module" src="http://127.0.0.1:3000/@vite/client"></script>'
        )
    return '' 