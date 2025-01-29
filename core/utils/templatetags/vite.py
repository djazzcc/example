from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
import json
import shutil
from pathlib import Path
import requests
from requests.exceptions import RequestException

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

def is_vite_running():
    """Check if Vite dev server is running"""
    try:
        response = requests.get('http://127.0.0.1:3000/static/@vite/client', timeout=0.5)
        return response.status_code == 200
    except RequestException:
        return False

@register.simple_tag
def vite_asset(path):
    """
    Resolve a Vite asset path based on manifest.json in development and production.
    """
    if settings.DEBUG:
        if is_vite_running():
            return f'http://127.0.0.1:3000/static/{path}'
        else:
            print("Warning: Vite dev server is not running. Please run 'pnpm dev'")
            # Fallback to production assets
            try:
                manifest_path = settings.STATIC_ROOT / '.vite/manifest.json'
                with open(manifest_path) as f:
                    manifest = json.load(f)

                entry_point = manifest["core/assets/js/main.js"]
                
                if path == 'css/main.css':
                    return f'/static/{entry_point["css"][0]}'
                elif path == 'js/main.js':
                    return f'/static/{entry_point["file"]}'
                
                return f'/static/{manifest[path]["file"]}'
            except (FileNotFoundError, KeyError) as e:
                print(f"Error loading asset {path}: {str(e)}")
                return f'/static/{path}'
    
    try:
        manifest_path = settings.STATIC_ROOT / '.vite/manifest.json'
        with open(manifest_path) as f:
            manifest = json.load(f)

        entry_point = manifest["core/assets/js/main.js"]
        
        if path == 'css/main.css':
            return f'/static/{entry_point["css"][0]}'
        elif path == 'js/main.js':
            return f'/static/{entry_point["file"]}'
        
        return f'/static/{manifest[path]["file"]}'
    except (FileNotFoundError, KeyError) as e:
        print(f"Error loading asset {path}: {str(e)}")
        return f'/static/{path}'

@register.simple_tag
def vite_hmr():
    """
    Include Vite HMR script in development.
    """
    if settings.DEBUG and is_vite_running():
        return mark_safe(
            '<script type="module" src="http://127.0.0.1:3000/static/@vite/client"></script>'
        )
    return '' 