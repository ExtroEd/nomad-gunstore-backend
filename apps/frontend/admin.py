from django.contrib import admin
from .models import SiteSettings, Icon


class IconInline(admin.StackedInline):
    model = Icon
    extra = 0
    readonly_fields = ['preview']
    fields = ['icon_type', 'svg_file', 'preview']

    def preview(self, obj):
        return obj.preview()

    preview.short_description = "Предпросмотр"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    inlines = [IconInline]
    list_display = ['site_name', 'logo_preview']
    readonly_fields = ['logo_preview']
    fields = [
        'site_name',
        ('logo', 'logo_preview'),
    ]

    def logo_preview(self, obj):
        return obj.logo_preview()

    logo_preview.short_description = "Текущий логотип"

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(Icon)
class IconAdmin(admin.ModelAdmin):
    list_display = ['icon_type', 'preview']
    readonly_fields = ['preview']
    fields = ['icon_type', 'svg_file', 'svg_code', 'preview']

    def preview(self, obj):
        return obj.preview()

    preview.short_description = "Предпросмотр"
