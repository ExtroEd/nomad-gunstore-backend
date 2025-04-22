from django.contrib import admin
from django import forms
from .models import Category, Product, ProductAttribute


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            self.fields['attributes'].initial = {
                "color": "black",
                "weight": "1.5kg"
            }

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        discount_price = cleaned_data.get('discount_price')

        if price is not None and price < 0:
            self.add_error(
                'price', 'The price cannot be negative.'
            )

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
        'name', 'category', 'price', 'discount_price', 'brand',
        'stock', 'is_deal_of_the_day', 'sku', 'mpn', 'upc'
    )
    list_filter = (
        'category', 'brand', 'is_clearance', 'is_deal_of_the_day', 'stock'
    )
    search_fields = (
        'name', 'brand', 'sku', 'mpn', 'upc'
    )
    inlines = [
        ProductAttributeInline
    ]
    autocomplete_fields = [
        'category'
    ]
    readonly_fields = [
        'created_at', 'sku', 'mpn', 'upc'
    ]
    fieldsets = (
        ('Общая информация', {
            'fields': (
                'name', 'category', 'brand', 'price', 'discount_price', 'image'
            )
        }),
        ('Описание', {
            'fields': (
                'details', 'features',
            )
        }),
        ('Системные идентификаторы', {
            'fields': (
                'sku', 'mpn', 'upc'
            )
        }),
        ('Дополнительно', {
            'fields': (
                'stock', 'is_clearance', 'is_deal_of_the_day', 'created_at'
            )
        }),
        ('Атрибуты', {
            'fields': ('attributes',)
        }),
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    autocomplete_fields = ['parent']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
