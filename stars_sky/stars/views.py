from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Star
from .serializers import (
    StarListSerializer,
    StarDetailSerializer,
    StarCreateUpdateSerializer,
)


class StarViewSet(viewsets.ModelViewSet):
    """
    API endpoint для звёзд.

    Фильтры:
      ?constellation=1
      ?spectral_class=G
      ?is_variable=true
    Поиск:
      ?search=Бетельгейзе
    Сортировка:
      ?ordering=apparent_magnitude
      ?ordering=-distance_ly
    """
    queryset = Star.objects.select_related('constellation').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['constellation', 'spectral_class', 'is_variable']
    search_fields = ['name', 'catalog_name', 'description']
    ordering_fields = ['name', 'apparent_magnitude', 'distance_ly', 'temperature']
    ordering = ['apparent_magnitude']

    def get_serializer_class(self):
        if self.action == 'list':
            return StarListSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return StarCreateUpdateSerializer
        return StarDetailSerializer
