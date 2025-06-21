from django.db import models
from django.utils.html import format_html
from django.core.validators import FileExtensionValidator


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="Nomad Tactical")
    logo = models.ImageField(
        upload_to='site_images/',
        blank=True,
        null=True,
        help_text="Логотип сайта (рекомендуемый размер: 200x50px)"
    )

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self):
        return "Настройки сайта"

    def logo_preview(self):
        if self.logo:
            return format_html(
                '<img src="{}" style="max-height: 50px;" />',
                self.logo.url
            )
        return "Логотип не загружен"

    logo_preview.short_description = "Предпросмотр логотипа"


class Icon(models.Model):
    ICON_TYPES = (
        ('search', 'Поиск'),
        ('login', 'Вход'),
        ('help', 'Помощь'),
        ('cart', 'Корзина'),
    )

    site_settings = models.ForeignKey(
        SiteSettings,
        on_delete=models.CASCADE,
        related_name='icons',
        verbose_name="Настройки сайта"
    )

    icon_type = models.CharField(
        max_length=20,
        choices=ICON_TYPES,
        unique=True,
        verbose_name="Тип иконки"
    )

    svg_file = models.FileField(
        upload_to='icons/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['svg'])],
        help_text="Загрузите SVG файл",
        verbose_name="SVG файл"
    )

    svg_code = models.TextField(
        blank=True,
        help_text="Или вставьте SVG код напрямую",
        verbose_name="SVG код"
    )

    class Meta:
        verbose_name = "Иконка"
        verbose_name_plural = "Иконки"

    def __str__(self):
        return self.get_icon_type_display()

    def get_svg(self):
        if self.svg_file:
            try:
                with open(self.svg_file.path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"Error reading SVG file: {e}")
                return ""
        return self.svg_code or ""

    def preview(self):
        if self.svg_file:
            return format_html(
                '<div style="width: 50px; height: 50px;">{}</div>',
                format_html(self.svg_file.read().decode())
            )
        elif self.svg_code:
            return format_html(
                '<div style="width: 50px; height: 50px;">{}</div>',
                self.svg_code
            )
        return "Нет данных для отображения"

    preview.short_description = "Предпросмотр"
