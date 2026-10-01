from django.db import models


class Constellation(models.Model):
    """Модель созвездия."""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название (лат.)',
        help_text='Латинское название созвездия'
    )
    name_ru = models.CharField(
        max_length=100,
        verbose_name='Название (рус.)',
        help_text='Русское название созвездия'
    )
    abbreviation = models.CharField(
        max_length=10,
        blank=True,
        verbose_name='Аббревиатура',
        help_text='Официальная аббревиатура (3 буквы)'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Подробное описание созвездия'
    )
    area = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Площадь (кв.градусов)',
        help_text='Площадь созвездия в квадратных градусах'
    )
    best_viewing_month = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=[(m, m) for m in range(1, 13)],
        verbose_name='Лучший месяц наблюдения',
        help_text='Месяц наилучшей видимости (1-12)'
    )
    is_zodiacal = models.BooleanField(
        default=False,
        verbose_name='Зодиакальное',
        help_text='Является ли созвездие зодиакальным'
    )
    is_visible_from_russia = models.BooleanField(
        default=True,
        verbose_name='Видимо из России',
        help_text='Видимо ли с территории России'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Созвездие'
        verbose_name_plural = 'Созвездия'
        ordering = ['name_ru']

    def __str__(self):
        return f'{self.name_ru} ({self.name})'

    @property
    def stars_count(self):
        return self.stars.count()


class ConstellationLine(models.Model):
    """Линия между звёздами в созвездии."""
    constellation = models.ForeignKey(
        Constellation,
        on_delete=models.CASCADE,
        related_name='lines',
        verbose_name='Созвездие'
    )
    star_from_name = models.CharField(
        max_length=100,
        verbose_name='Звезда (от)'
    )
    star_to_name = models.CharField(
        max_length=100,
        verbose_name='Звезда (до)'
    )

    class Meta:
        verbose_name = 'Линия созвездия'
        verbose_name_plural = 'Линии созвездий'
        ordering = ['constellation']

    def __str__(self):
        return f'{self.constellation.name_ru}: {self.star_from_name} → {self.star_to_name}'
