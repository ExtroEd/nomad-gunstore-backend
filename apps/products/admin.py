from functools import lru_cache
from django import forms
from django.contrib import admin, messages
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.html import format_html

from .models import Product, Category, ProductAttribute


@lru_cache(maxsize=None)
def get_content_type(model):
    return ContentType.objects.get_for_model(model)


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk and 'attributes' in self.fields:
            self.fields['attributes'].initial = {
                "color": "black",
                "weight": "1.5kg"
            }

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        discount_price = cleaned_data.get('discount_price')

        if price is not None and price < 0:
            self.add_error('price', 'The price cannot be negative.')

        if discount_price is not None and price is not None:
            if discount_price > price:
                raise forms.ValidationError(
                    "The discount price cannot be higher than the regular "
                    "price."
                )

        return cleaned_data


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = (
        'id', 'name', 'category', 'price', 'discount_price', 'brand',
        'quantity', 'stock', 'is_deal_of_the_day', 'sku', 'mpn', 'upc'
    )
    list_filter = (
        'id', 'category', 'brand', 'is_clearance', 'is_deal_of_the_day',
        'stock'
    )
    search_fields = (
        'id', 'name', 'brand', 'sku', 'mpn', 'upc'
    )
    inlines = [ProductAttributeInline]
    autocomplete_fields = ['category']
    readonly_fields = [
        'id', 'created_at', 'sku', 'mpn', 'upc', 'stock', 'log_history_link'
    ]

    fieldsets = (
        ('Общая информация', {
            'fields': (
                'id', 'name', 'category', 'brand', 'price', 'discount_price',
                'image'
            )
        }),
        ('Описание', {
            'fields': ('details', 'features',)
        }),
        ('Системные идентификаторы', {
            'fields': ('sku', 'mpn', 'upc')
        }),
        ('Дополнительно', {
            'fields': (
                'quantity', 'stock', 'is_clearance', 'is_deal_of_the_day',
                'created_at'
            )
        }),
        ('Атрибуты', {
            'fields': ('attributes',)
        }),
    )

    def log_history_link(self, obj):
        content_type = get_content_type(obj.__class__)
        url = reverse("admin:admin_logentry_changelist") + \
              f"?content_type__id__exact={content_type.id}&object_id={obj.id}"
        return format_html(f'<a href="{url}">📜 История</a>')

    log_history_link.short_description = "Логи изменений"

    def delete_model(self, request, obj):
        affected_items = obj.cart_items.count()
        if affected_items:
            self.message_user(
                request,
                f"Удалено {affected_items} позиций из корзин вместе с "
                f"продуктом.",
                level=messages.WARNING
            )
        super().delete_model(request, obj)


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


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'action_time', 'user', 'content_type', 'object_repr',
        'action_flag'
    )
    list_filter = ('action_flag', 'content_type', 'user')
    search_fields = ('object_repr', 'change_message')
    date_hierarchy = 'action_time'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
