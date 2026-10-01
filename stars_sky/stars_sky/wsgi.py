"""
WSGI config for stars_sky project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stars_sky.settings')
application = get_wsgi_application()
