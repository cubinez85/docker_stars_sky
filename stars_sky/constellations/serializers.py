from rest_framework import serializers
from .models import Constellation, ConstellationLine


class ConstellationLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstellationLine
        fields = ['id', 'star_from_name', 'star_to_name']


class ConstellationListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка созвездий."""
    stars_count = serializers.ReadOnlyField()

    class Meta:
        model = Constellation
        fields = [
            'id', 'name', 'name_ru', 'abbreviation',
            'is_zodiacal', 'is_visible_from_russia',
            'best_viewing_month', 'stars_count',
        ]


class ConstellationDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детального просмотра созвездия."""
    lines = ConstellationLineSerializer(many=True, read_only=True)
    stars_count = serializers.ReadOnlyField()

    class Meta:
        model = Constellation
        fields = [
            'id', 'name', 'name_ru', 'abbreviation',
            'description', 'area', 'best_viewing_month',
            'is_zodiacal', 'is_visible_from_russia',
            'stars_count', 'lines',
            'created_at', 'updated_at',
        ]


class ConstellationCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления созвездия."""

    class Meta:
        model = Constellation
        fields = [
            'name', 'name_ru', 'abbreviation',
            'description', 'area', 'best_viewing_month',
            'is_zodiacal', 'is_visible_from_russia',
        ]
