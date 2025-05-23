from functools import lru_cache

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.html import format_html

from apps.categories.models import Category


@lru_cache(maxsize=None)
def get_content_type(model):
    return ContentType.objects.get_for_model(model, for_concrete_model=False)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name', 'slug']
    readonly_fields = ['id', 'log_history_link', 'image_preview']

    list_display = [
        'id', 'name', 'slug', 'parent', 'image_preview', 'log_history_link'
    ]
    autocomplete_fields = ['parent']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 40px;"/>',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Изображение"

    def log_history_link(self, obj):
        content_type = get_content_type(obj.__class__)
        url = (
            reverse("admin:admin_logentry_changelist") +
            f"?content_type__id__exact={content_type.id}&object_id={obj.id}"
        )
        return format_html('<a href="{}">📜 История</a>', url)
    log_history_link.short_description = "Логи изменений"
