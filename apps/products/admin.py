from functools import lru_cache
from django import forms
from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html

from .models import Product, ProductAttribute
from apps.categories.models import Category
from apps.categories.admin import CategoryAdmin


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


class RoundCountFilter(SimpleListFilter):
    title = 'Количество патронов'
    parameter_name = 'round_count'

    def lookups(self, request, model_admin):
        values = (
            ProductAttribute.objects
            .filter(key__iexact='round count')
            .values_list('value', flat=True)
            .distinct()
            .order_by('value')
        )
        return [(v, f"{v} шт.") for v in values if v.isdigit()]

    def queryset(self, request, queryset):
        value = self.value()
        if value and value.isdigit():
            return queryset.filter(
                attribute_set__key__iexact='round count',
                attribute_set__value=value
            ).distinct()
        return queryset


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = (
        'id', 'name', 'category', 'price', 'discount_price', 'brand',
        'quantity', 'stock', 'is_deal_of_the_day', 'sku', 'mpn', 'upc'
    )
    list_filter = (
        'id', 'category', 'brand', 'is_clearance', 'is_deal_of_the_day',
        'stock', RoundCountFilter
    )
    search_fields = (
        'id', 'name', 'brand', 'sku', 'mpn', 'upc'
    )
    inlines = [
        ProductAttributeInline
    ]
    autocomplete_fields = [
        'category'
    ]
    readonly_fields = [
        'id', 'created_at', 'sku', 'mpn', 'upc', 'stock', 'log_history_link',
        'price_per_round'
    ]
    fieldsets = (
        ('Общая информация', {
            'fields': (
                'id', 'name', 'category', 'brand', 'price', 'discount_price',
                'image', 'shipping_price'
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
                'quantity', 'stock', 'price_per_round', 'is_clearance',
                'is_deal_of_the_day', 'created_at'
            )
        }),
    )

    def get_search_results(self, request, queryset, search_term):
        base_queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )

        attr_filter = Q(attribute_set__key__icontains=search_term) | Q(
            attribute_set__value__icontains=search_term)
        attr_matches = Product.objects.filter(attr_filter)

        combined = base_queryset | attr_matches
        return combined.distinct(), True

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

    def price_per_round(self, obj):
        price = obj.get_price_per_round()
        return f"${price:.2f}" if price is not None else "N/A"

    price_per_round.short_description = "Price per Round"


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
