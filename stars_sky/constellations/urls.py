from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConstellationViewSet

router = DefaultRouter()
router.register(r'', ConstellationViewSet, basename='constellation')

urlpatterns = [
    path('', include(router.urls)),
]
