from django.db import models
from constellations.models import Constellation


class Star(models.Model):
    """Модель звезды."""

    SPECTRAL_CLASSES = [
        ('O', 'O — голубая (>30000K)'),
        ('B', 'B — голубовато-белая (10000-30000K)'),
        ('A', 'A — белая (7500-10000K)'),
        ('F', 'F — жёлто-белая (6000-7500K)'),
        ('G', 'G — жёлтая (5200-6000K)'),
        ('K', 'K — оранжевая (3700-5200K)'),
        ('M', 'M — красная (2400-3700K)'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Общепринятое имя звезды (например, Бетельгейзе)'
    )
    catalog_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Каталожное имя',
        help_text='Название по каталогу (например, α Ori)'
    )
    constellation = models.ForeignKey(
        Constellation,
        on_delete=models.CASCADE,
        related_name='stars',
        verbose_name='Созвездие'
    )
    right_ascension = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Прямое восхождение',
        help_text='Прямое восхождение в часах (0-24)'
    )
    declination = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Склонение',
        help_text='Склонение в градусах (-90 до +90)'
    )
    apparent_magnitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Видимая звёздная величина',
        help_text='Чем меньше число, тем ярче звезда'
    )
    absolute_magnitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Абсолютная звёздная величина'
    )
    distance_ly = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Расстояние (св.лет)',
        help_text='Расстояние в световых годах'
    )
    temperature = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Температура (K)',
        help_text='Эффективная температура поверхности в Кельвинах'
    )
    spectral_class = models.CharField(
        max_length=1,
        choices=SPECTRAL_CLASSES,
        blank=True,
        verbose_name='Спектральный класс'
    )
    color_hex = models.CharField(
        max_length=7,
        default='#ffffff',
        verbose_name='Цвет (HEX)',
        help_text='HEX-код цвета звезды для отображения'
    )
    position_x = models.FloatField(
        default=0.5,
        verbose_name='Позиция X (0-1)',
        help_text='Нормализованная координата X на карте'
    )
    position_y = models.FloatField(
        default=0.5,
        verbose_name='Позиция Y (0-1)',
        help_text='Нормализованная координата Y на карте'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    is_variable = models.BooleanField(
        default=False,
        verbose_name='Переменная звезда'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Звезда'
        verbose_name_plural = 'Звёзды'
        ordering = ['apparent_magnitude']
        indexes = [
            models.Index(fields=['constellation']),
            models.Index(fields=['spectral_class']),
            models.Index(fields=['apparent_magnitude']),
        ]

    def __str__(self):
        return f'{self.name} ({self.constellation.name_ru})'

    @property
    def display_size(self):
        """Размер для отображения на карте (1-5)."""
        if self.apparent_magnitude is None:
            return 2
        if self.apparent_magnitude < 0:
            return 5
        if self.apparent_magnitude < 1:
            return 4
        if self.apparent_magnitude < 2:
            return 3
        if self.apparent_magnitude < 4:
            return 2
        return 1
