from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Constellation
from .serializers import (
    ConstellationListSerializer,
    ConstellationDetailSerializer,
    ConstellationCreateUpdateSerializer,
)


class ConstellationViewSet(viewsets.ModelViewSet):
    """
    API endpoint для созвездий.

    list:   GET    /api/constellations/
    create: POST   /api/constellations/
    read:   GET    /api/constellations/{id}/
    update: PUT    /api/constellations/{id}/
    patch:  PATCH  /api/constellations/{id}/
    delete: DELETE /api/constellations/{id}/

    Фильтры:
      ?is_zodiacal=true
      ?is_visible_from_russia=true
      ?best_viewing_month=6
    Поиск:
      ?search=Орион
    Сортировка:
      ?ordering=name_ru
    """
    queryset = Constellation.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_zodiacal', 'is_visible_from_russia', 'best_viewing_month']
    search_fields = ['name', 'name_ru', 'description']
    ordering_fields = ['name', 'name_ru', 'area', 'created_at']
    ordering = ['name_ru']

    def get_serializer_class(self):
        if self.action == 'list':
            return ConstellationListSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return ConstellationCreateUpdateSerializer
        return ConstellationDetailSerializer
