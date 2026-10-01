from rest_framework import serializers
from .models import Star


class StarListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка звёзд."""
    constellation_name = serializers.CharField(source='constellation.name_ru', read_only=True)
    display_size = serializers.ReadOnlyField()

    class Meta:
        model = Star
        fields = [
            'id', 'name', 'catalog_name', 'constellation',
            'constellation_name', 'apparent_magnitude',
            'color_hex', 'position_x', 'position_y',
            'display_size', 'is_variable',
        ]


class StarDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детального просмотра звезды."""
    constellation_name = serializers.CharField(source='constellation.name_ru', read_only=True)
    display_size = serializers.ReadOnlyField()

    class Meta:
        model = Star
        fields = [
            'id', 'name', 'catalog_name',
            'constellation', 'constellation_name',
            'right_ascension', 'declination',
            'apparent_magnitude', 'absolute_magnitude',
            'distance_ly', 'temperature', 'spectral_class',
            'color_hex', 'position_x', 'position_y',
            'description', 'is_variable', 'display_size',
            'created_at', 'updated_at',
        ]


class StarCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления звезды."""

    class Meta:
        model = Star
        fields = [
            'name', 'catalog_name', 'constellation',
            'right_ascension', 'declination',
            'apparent_magnitude', 'absolute_magnitude',
            'distance_ly', 'temperature', 'spectral_class',
            'color_hex', 'position_x', 'position_y',
            'description', 'is_variable',
        ]
