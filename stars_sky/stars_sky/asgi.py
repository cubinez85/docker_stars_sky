"""
ASGI config for stars_sky project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stars_sky.settings')
application = get_asgi_application()
