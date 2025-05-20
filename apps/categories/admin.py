from functools import lru_cache

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.html import format_html


@lru_cache(maxsize=None)
def get_content_type(model):
    return ContentType.objects.get_for_model(model)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent')
    search_fields = ('id', 'name')
    autocomplete_fields = ['parent']
    readonly_fields = ['id', 'log_history_link']

    def log_history_link(self, obj):
        content_type = get_content_type(obj.__class__)
        url = reverse("admin:admin_logentry_changelist") + \
              f"?content_type__id__exact={content_type.id}&object_id={obj.id}"
        return format_html(f'<a href="{url}">📜 История</a>')

    log_history_link.short_description = "Логи изменений"
