import logging
from pathlib import Path
from typing import Optional

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
import json
import shutil
import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)
register = template.Library()

VITE_DEV_SERVER = "http://127.0.0.1:3000"
VITE_MANIFEST_PATH = ".vite/manifest.json"
ENTRY_POINT = "core/assets/js/main.js"

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

def get_manifest_data() -> Optional[dict]:
    """Get manifest data from the manifest file"""
    try:
        manifest_path = settings.STATIC_ROOT / VITE_MANIFEST_PATH
        with open(manifest_path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.warning(f"Failed to load manifest file: {e}")
        return None

def is_vite_running() -> bool:
    """Check if Vite dev server is running"""
    try:
        response = requests.get(f"{VITE_DEV_SERVER}/static/@vite/client", timeout=0.5)
        return response.status_code == 200
    except RequestException:
        return False

def get_dev_asset_url(path: str) -> str:
    """Get asset URL for development"""
    return f"{VITE_DEV_SERVER}/static/{path}"

def get_prod_asset_url(path: str, manifest_data: dict) -> str:
    """Get asset URL for production"""
    try:
        entry_point = manifest_data[ENTRY_POINT]
        
        if path == 'css/main.css':
            return f'/static/{entry_point["css"][0]}'
        elif path == 'js/main.js':
            return f'/static/{entry_point["file"]}'
        
        return f'/static/{manifest_data[path]["file"]}'
    except KeyError as e:
        logger.error(f"Failed to find asset {path} in manifest: {e}")
        return f'/static/{path}'

@register.simple_tag
def vite_asset(path: str) -> str:
    """
    Resolve a Vite asset path based on manifest.json in development and production.
    
    Args:
        path: The path to the asset relative to the assets directory
        
    Returns:
        str: The URL to the asset
    """
    if settings.DEBUG:
        if is_vite_running():
            return get_dev_asset_url(path)
        else:
            logger.warning("Vite dev server is not running. Please run 'pnpm dev'")
            # Fallback to production assets
            manifest_data = get_manifest_data()
            if manifest_data:
                return get_prod_asset_url(path, manifest_data)
            return f'/static/{path}'
    
    manifest_data = get_manifest_data()
    if manifest_data:
        return get_prod_asset_url(path, manifest_data)
    return f'/static/{path}'

@register.simple_tag
def vite_hmr() -> str:
    """
    Include Vite HMR script in development.
    
    Returns:
        str: The HMR script tag or empty string in production
    """
    if settings.DEBUG and is_vite_running():
        return mark_safe(
            f'<script type="module" src="{VITE_DEV_SERVER}/static/@vite/client"></script>'
        )
    return '' 