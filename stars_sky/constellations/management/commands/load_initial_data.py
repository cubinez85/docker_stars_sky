"""
Management-команда для загрузки начальных данных о созвездиях и звёздах.
Запуск: python manage.py load_initial_data
"""
from django.core.management.base import BaseCommand
from constellations.models import Constellation, ConstellationLine
from stars.models import Star


class Command(BaseCommand):
    help = 'Загружает начальные данные о созвездиях и звёздах'

    def handle(self, *args, **options):
        self.stdout.write('Загрузка начальных данных...')

        # === Созвездия ===
        constellations_data = [
            {
                'name': 'Orion',
                'name_ru': 'Орион',
                'abbreviation': 'Ori',
                'description': 'Одно из самых узнаваемых созвездий. Видно из обоих полушарий. Содержит туманность Ориона (M42).',
                'area': 594.0,
                'best_viewing_month': 1,
                'is_zodiacal': False,
                'is_visible_from_russia': True,
            },
            {
                'name': 'Ursa Major',
                'name_ru': 'Большая Медведица',
                'abbreviation': 'UMa',
                'description': 'Содержит знаменитый астеризм Большой Ковш. Помогает найти Полярную звезду.',
                'area': 1280.0,
                'best_viewing_month': 4,
                'is_zodiacal': False,
                'is_visible_from_russia': True,
            },
            {
                'name': 'Cassiopeia',
                'name_ru': 'Кассиопея',
                'abbreviation': 'Cas',
                'description': 'W-образное созвездие, видимое круглый год в северном полушарии. Названо в честь эфиопской царицы.',
                'area': 598.0,
                'best_viewing_month': 11,
                'is_zodiacal': False,
                'is_visible_from_russia': True,
            },
            {
                'name': 'Leo',
                'name_ru': 'Лев',
                'abbreviation': 'Leo',
                'description': 'Одно из зодиакальных созвездий. Связано с Немейским львом из греческой мифологии.',
                'area': 947.0,
                'best_viewing_month': 4,
                'is_zodiacal': True,
                'is_visible_from_russia': True,
            },
            {
                'name': 'Scorpius',
                'name_ru': 'Скорпион',
                'abbreviation': 'Sco',
                'description': 'Яркое созвездие южного неба. Антарес — красный сверхгигант, соперник Марса по яркости.',
                'area': 497.0,
                'best_viewing_month': 7,
                'is_zodiacal': True,
                'is_visible_from_russia': False,
            },
            {
                'name': 'Cygnus',
                'name_ru': 'Лебедь',
                'abbreviation': 'Cyg',
                'description': 'Крестообразное созвездие, лежащее на Млечном Пути. Денеб — одна из вершин Летнего треугольника.',
                'area': 804.0,
                'best_viewing_month': 9,
                'is_zodiacal': False,
                'is_visible_from_russia': True,
            },
        ]

        constellation_objects = {}
        for data in constellations_data:
            obj, created = Constellation.objects.update_or_create(
                name=data['name'],
                defaults=data,
            )
            constellation_objects[data['name']] = obj
            status = 'создано' if created else 'обновлено'
            self.stdout.write(f'  Созвездие {obj.name_ru} — {status}')

        # === Звёзды ===
        stars_data = [
            # Орион
            {'name': 'Бетельгейзе', 'constellation': 'Orion', 'apparent_magnitude': 0.42, 'color_hex': '#ff6b35', 'position_x': 0.45, 'position_y': 0.20, 'spectral_class': 'M', 'temperature': 3600, 'distance_ly': 700, 'catalog_name': 'α Ori'},
            {'name': 'Ригель', 'constellation': 'Orion', 'apparent_magnitude': 0.13, 'color_hex': '#4fc3f7', 'position_x': 0.58, 'position_y': 0.22, 'spectral_class': 'B', 'temperature': 12100, 'distance_ly': 860, 'catalog_name': 'β Ori'},
            {'name': 'Беллатрикс', 'constellation': 'Orion', 'apparent_magnitude': 1.64, 'color_hex': '#add8e6', 'position_x': 0.55, 'position_y': 0.18, 'spectral_class': 'B', 'temperature': 21500, 'distance_ly': 250, 'catalog_name': 'γ Ori'},
            # Большая Медведица
            {'name': 'Дубхе', 'constellation': 'Ursa Major', 'apparent_magnitude': 1.79, 'color_hex': '#ffe4c4', 'position_x': 0.15, 'position_y': 0.15, 'spectral_class': 'K', 'temperature': 4660, 'distance_ly': 123, 'catalog_name': 'α UMa'},
            {'name': 'Мерак', 'constellation': 'Ursa Major', 'apparent_magnitude': 2.37, 'color_hex': '#ffffff', 'position_x': 0.20, 'position_y': 0.13, 'spectral_class': 'A', 'temperature': 9370, 'distance_ly': 79, 'catalog_name': 'β UMa'},
            {'name': 'Мицар', 'constellation': 'Ursa Major', 'apparent_magnitude': 2.27, 'color_hex': '#ffffff', 'position_x': 0.32, 'position_y': 0.12, 'spectral_class': 'A', 'temperature': 9000, 'distance_ly': 78, 'catalog_name': 'ζ UMa'},
            # Кассиопея
            {'name': 'Шедар', 'constellation': 'Cassiopeia', 'apparent_magnitude': 2.24, 'color_hex': '#ffe4c4', 'position_x': 0.70, 'position_y': 0.12, 'spectral_class': 'K', 'temperature': 4530, 'distance_ly': 228, 'catalog_name': 'α Cas'},
            {'name': 'Гамма Кассиопеи', 'constellation': 'Cassiopeia', 'apparent_magnitude': 2.47, 'color_hex': '#add8e6', 'position_x': 0.73, 'position_y': 0.08, 'spectral_class': 'B', 'temperature': 12000, 'distance_ly': 550, 'catalog_name': 'γ Cas', 'is_variable': True},
            # Лев
            {'name': 'Регул', 'constellation': 'Leo', 'apparent_magnitude': 1.35, 'color_hex': '#90caf9', 'position_x': 0.60, 'position_y': 0.60, 'spectral_class': 'B', 'temperature': 12460, 'distance_ly': 79, 'catalog_name': 'α Leo'},
            {'name': 'Денебола', 'constellation': 'Leo', 'apparent_magnitude': 2.14, 'color_hex': '#ffffff', 'position_x': 0.75, 'position_y': 0.58, 'spectral_class': 'A', 'temperature': 8500, 'distance_ly': 36, 'catalog_name': 'β Leo'},
            # Скорпион
            {'name': 'Антарес', 'constellation': 'Scorpius', 'apparent_magnitude': 1.06, 'color_hex': '#ff5252', 'position_x': 0.20, 'position_y': 0.60, 'spectral_class': 'M', 'temperature': 3660, 'distance_ly': 550, 'catalog_name': 'α Sco', 'is_variable': True},
            # Лебедь
            {'name': 'Денеб', 'constellation': 'Cygnus', 'apparent_magnitude': 1.25, 'color_hex': '#e3f2fd', 'position_x': 0.85, 'position_y': 0.35, 'spectral_class': 'A', 'temperature': 8525, 'distance_ly': 2615, 'catalog_name': 'α Cyg'},
        ]

        for data in stars_data:
            constellation = constellation_objects[data.pop('constellation')]
            star, created = Star.objects.update_or_create(
                name=data['name'],
                constellation=constellation,
                defaults={**data, 'constellation': constellation},
            )
            status = 'создана' if created else 'обновлена'
            self.stdout.write(f'  Звезда {star.name} — {status}')

        # === Линии созвездий ===
        lines_data = {
            'Orion': [
                ('Бетельгейзе', 'Беллатрикс'),
                ('Бетельгейзе', 'Ригель'),
            ],
            'Ursa Major': [
                ('Дубхе', 'Мерак'),
                ('Мерак', 'Мицар'),
            ],
            'Cassiopeia': [
                ('Шедар', 'Гамма Кассиопеи'),
            ],
            'Leo': [
                ('Регул', 'Денебола'),
            ],
        }

        for const_name, lines in lines_data.items():
            constellation = constellation_objects[const_name]
            for from_name, to_name in lines:
                _, created = ConstellationLine.objects.get_or_create(
                    constellation=constellation,
                    star_from_name=from_name,
                    star_to_name=to_name,
                )
                if created:
                    self.stdout.write(f'  Линия: {from_name} → {to_name}')

        self.stdout.write(self.style.SUCCESS('✅ Начальные данные успешно загружены!'))
