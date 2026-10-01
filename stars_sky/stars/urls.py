from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StarViewSet

router = DefaultRouter()
router.register(r'', StarViewSet, basename='star')

urlpatterns = [
    path('', include(router.urls)),
]
