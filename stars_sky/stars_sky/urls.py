"""stars_sky URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import api_root, health_check

urlpatterns = [
    path('', api_root, name='api-root'),
    path('health', health_check, name='health-check'),
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-info'),
    path('api/constellations/', include('constellations.urls')),
    path('api/stars/', include('stars.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


"""stars_sky URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import api_root, health_check, sky_view

urlpatterns = [
    path('', api_root, name='api-root'),
    path('sky/', sky_view, name='sky'),
    path('health', health_check, name='health-check'),
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-info'),
    path('api/constellations/', include('constellations.urls')),
    path('api/stars/', include('stars.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
