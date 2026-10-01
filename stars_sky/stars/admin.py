from django.contrib import admin
from .models import Star


@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    list_display = ['name', 'constellation', 'apparent_magnitude', 'spectral_class', 'distance_ly', 'is_variable']
    list_filter = ['constellation', 'spectral_class', 'is_variable']
    search_fields = ['name', 'catalog_name', 'description']
