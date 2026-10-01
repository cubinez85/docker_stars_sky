from django.contrib import admin
from .models import Constellation, ConstellationLine


class ConstellationLineInline(admin.TabularInline):
    model = ConstellationLine
    extra = 1


@admin.register(Constellation)
class ConstellationAdmin(admin.ModelAdmin):
    list_display = ['name_ru', 'name', 'abbreviation', 'is_zodiacal', 'is_visible_from_russia', 'best_viewing_month']
    list_filter = ['is_zodiacal', 'is_visible_from_russia', 'best_viewing_month']
    search_fields = ['name', 'name_ru', 'description']
    inlines = [ConstellationLineInline]


@admin.register(ConstellationLine)
class ConstellationLineAdmin(admin.ModelAdmin):
    list_display = ['constellation', 'star_from_name', 'star_to_name']
    list_filter = ['constellation']
