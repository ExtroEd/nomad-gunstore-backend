from django.utils.html import format_html
from django.contrib import admin

from apps.frontend.models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    readonly_fields = [
        'preview_icon_login'
    ]
    fields = [
        'site_name', 'logo', 'icon_login', 'icon_help', 'icon_cart',
        'icon_search'
    ]

    def preview_icon_login(self, obj):
        if obj.icon_login:
            content = obj.icon_login.read().decode()
            return format_html(content)
        return "No icon"
